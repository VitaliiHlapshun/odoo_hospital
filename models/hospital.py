# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Hospital(models.Model):
    _name = 'hospital.hospital'
    _description = 'hospital.hospital'
    _rec_name = 'first_name'  # to make first name shown as a record
    _inherit = ['mail.thread', 'mail.activity.mixin']  # adding chatter

    @api.depends('age')
    def age_group_definition(self):
        for rec in self:
            if rec.age >= 18:
                rec.age_group = "major"
            else:
                rec.age_group = "minor"

    first_name = fields.Char(string="First Name")
    last_name = fields.Char(required=True)
    age = fields.Integer()
    image = fields.Binary()
    name_seq = fields.Char(string='Order Reference', required=True, copy=False, readonly=True, index=True,
                           default=lambda self: _('New'))

    age_group = fields.Selection([
        ('major', 'Major'),
        ('minor', 'Minor')], string="Age Group", compute='age_group_definition', default=False)

    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('hospital.patient.sequence') or _('New')

        result = super(Hospital, self).create(vals)
        return result
