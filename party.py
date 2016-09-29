# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import ModelSQL, ModelView, fields
from trytond.pool import PoolMeta
from trytond.transaction import Transaction

__all__ = ['Cnae', 'Party']


class Cnae(ModelSQL, ModelView):
    '''CNAE'''
    __name__ = 'party.cnae'
    _order = 'code'

    code = fields.Char('Code', required=True)
    name = fields.Char('Name', required=True)
    parent = fields.Many2One('party.cnae', 'Parent', select=True)
    childs = fields.One2Many('party.cnae', 'parent', string='Children')
    full_name = fields.Function(fields.Char('Full Name'),
        'get_full_name')

    @classmethod
    def validate(cls, cnaes):
        super(Cnae, cls).validate(cnaes)
        cls.check_recursion(cnaes, rec_name='name')

    def get_rec_name(self, name):
        return u"[%s] %s" % (self.code, self.name)

    @classmethod
    def search_rec_name(cls, name, clause):
        return ['OR',
            ('code',) + tuple(clause[1:]),
            ('name',) + tuple(clause[1:]),
            ]

    def get_full_name(self, name):
        res = self.rec_name
        parent = self.parent
        while parent:
            res = u'%s / %s' % (parent.name, res)
            parent = parent.parent
        return res


class Party:
    __name__ = 'party.party'
    __metaclass__ = PoolMeta

    cnae = fields.Many2One('party.cnae', 'CNAE')

    @staticmethod
    def default_cnae():
        return Transaction().context.get('cnae')
