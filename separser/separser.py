import argparse
import logging
import sys
import shlex

import sepol


RESERVED = set(["{","}",":",";", "-"])


class SEParser(object):

    def __init__(self, source):
        self.policy = sepol.SEPolicy()
        self.lexer = shlex.shlex(source)
        """
        Handle negations
        """
        self.lexer.wordchars += "-"
        """
        Track parsing parens/braces/brackets/what-have-you
        """
        self.stack = []

    def get_token(self):
        try:
            token = self.lexer.get_token()
        except ValueError:
            """
            Missing closing quotes
            """
            return ""
        else:
            return token

    def parse(self):
        for token in iter(self.get_token, ""):
            if token == "allow":
                self.parse_allow_rule()

    def parse_allow_rule(self):
        sources = self.parse_open_close()
        logging.debug("SRC: %s" % sources)

        targets = self.parse_open_close()
        logging.debug("TRG: %s" % targets)

        if not self.consume(":"):
            logging.error("Error in target:class at allow rule: allow %s %s" % (sources, targets))
            return None

        classes = self.parse_open_close()
        if classes == False:
            logging.error("Error in target:class at allow rule: allow %s %s" % (sources, targets))
            return None

        perms = self.parse_open_close()
        if perms == False:
            """
            This needs to be False, not "if not perms" which would match
            on empty permission sets.
            """
            logging.error("Error in permissions at allow rule: allow %s %s:%s" % (sources, targets, classes))
            return None

        if not self.consume(";"):
            logging.error("Missing closing semicolon at  allow rule: allow %s %s:%s {%s}" % (sources, target, classes, perms))
            return None

        for source in sources:
            if source.startswith("-"):
                # TODO: Handle type and attribute negations!
                continue
            for target in targets:
                if target.startswith("-"):
                    # TODO: Handle type and attribute negations!
                    continue
                for cls in classes:
                    if cls.startswith("-"):
                        # TODO: Handle type and attribute negations!
                        continue
                    rule = sepol.AllowRule(source, target, cls, perms)
                    self.policy.add_rule(rule)
                    logging.debug("%s" % rule)


    def parse_open_close(self):
        perms = []
        for token in iter(self.get_token, ""):
            if token == "}":
                try:
                    self.stack.pop()
                except IndexError:
                    logging.error("Mismatched open/close delims in permissions list")
                    return False
            elif token == "{":
                self.stack.append(token)
                perms.extend(self.parse_open_close())
            else:
                perms.append(token)
            if not self.stack:
                if token == ";" or token == ":":
                    perms = perms[:-1]
                    self.lexer.push_token(token)
                break
        return perms

    def consume(self, char):
        seen = False
        for token in iter(self.get_token, ""):
            if token != char:
                self.lexer.push_token(token)
                break
            seen = True
        return seen


def get_cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("fin",
                        help="Input file to parse", type=argparse.FileType("r"))
    parser.add_argument("-d", "--debug",
                        action="store_true", default=False)
    return parser.parse_args()


if __name__ == "__main__":
    cli_args = get_cli_args()
    if cli_args.debug:
        logging.basicConfig(level=logging.DEBUG)
    separser = SEParser(cli_args.fin.read())
    separser.parse()
