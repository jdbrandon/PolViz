import logging


class SEPolicy(object):

    def __init__(self):
        self.allows = {}
        self.neverallows = {}

    def add_rule(self, sepol_rule):
        if sepol_rule.rule_type == "allow":
            self.allow(sepol_rule)
        elif sepol_rule.rule_type == "neverallow":
            logging.warn("Not implemented: neverallow rule")
        else:
            logging.error("Unknown rule type: %s" % sepol_rule)

    def allow(self, rule):
        try:
            self.allows[rule.source]["%s:%s" % (rule.target, rule.target_class)] = rule.perms
        except KeyError:
            self.allows[rule.source] = {}
            self.allows[rule.source]["%s:%s" % (rule.target, rule.target_class)] = rule.perms


class Rule(object):
    rule_type = "base"

    
class AllowRule(Rule):
    rule_type = "allow"

    def __init__(self, src, trg, trg_class, perms):
        self.source = Domain(src)
        self.target = Type(trg)
        self.target_class = TypeClass(trg_class)
        self.perms = [Permission(p) for p in perms]

    def __str__(self):
        return "Parsed\n\tsource: %s\n\ttarget: %s\n\ttarget class: %s\n\tpermissions: %s\n" % (self.source, self.target, self.target_class, ",".join([str(p) for p in self.perms]))


class NeverAllowRule(Rule):
    ruletype = "neverallow"


class SEPolicyObject(object):

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Type(SEPolicyObject):
    pass


class Domain(Type):
    pass


class Attribute(SEPolicyObject):
    pass


class TypeClass(SEPolicyObject):
    pass    


class Permission(SEPolicyObject):
    pass
