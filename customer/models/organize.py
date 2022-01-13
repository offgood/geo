import logging
from odoo import models, fields, api
# บริษัท
_logger = logging.getLogger(__name__)
class Organizadetails(models.Model):
    _name = 'customer.organize'
    _description = 'Organize Details'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _rec_name = 'company_name'


    company_name = fields.Char(string='ชื่อบริษัท/หน่วยงาน', tracking=True, required=True) 
    logo = fields.Binary(string='', tracking=True)
    
    address = fields.Many2one('res.city.zip',string='ที่อยู่', tracking=True, required=True)
    post_code = fields.Char(string='รหัสไปรษณี', related='address.name', readonly=False, tracking=True, required=True)
    district = fields.Char(string='เขต', readonly=False, tracking=True, required=True)
    country_id = fields.Many2one('res.country', ondelete='restrict', related='address.country_id', readonly=False, string='ประเทศ', tracking=True,required=True)
    post_code = fields.Char(string='รหัสไปรษณี', readonly=False, tracking=True, required=True)
    Note_address = fields.Text(string='รายละเอียดที่อยู่', tracking=True)
    state_id = fields.Many2one(
        "res.country.state", string='จังหวัด', related='address.state_id',readonly=False, tracking=True)

    contacts_id = fields.One2many('customer.customers', 'company_id', tracking=True) 
    
    type_organize = fields.Many2one('customer.organize.typeor', string='ประเภท', tracking=True)
    website = fields.Char(string='เว็บไซต์', tracking=True)
    
    
    e_mail = fields.Char(string='อีเมล์', tracking=True, required=True)
    mobile = fields.Char(string='เบอร์มือถือ', tracking=True)
    phone = fields.Char(string='เบอร์โทรศัพท์', tracking=True, required=True)
    fax = fields.Char(string='แฟกซ์', tracking=True)
    line_id = fields.Char(string='Line ID', tracking=True)
    address_info = fields.Text(string='ที่อยู่ จัดส่ง', tracking=True)
    address_invoice_info = fields.Text(string='ที่อยู่ ตามใบเสร็จ', tracking=True)
    user_id = fields.Many2one('res.users', string='ผู้สร้าง', readonly=True, tracking=True, default=lambda self: self.env.user)
    
    # Address invoices
    street_invoice = fields.Many2one('res.city.zip','ที่อยู่(เลือก)',tracking=True)
    zip_invoice = fields.Char('รหัสไปรษณี',related='street_invoice.name', tracking=True,change_default=True, compute='_compute_partner_address_values', readonly=False, store=True)
    state_id_invoice = fields.Many2one(
        "res.country.state", string='จังหวัด', related='street_invoice.state_id',tracking=True,readonly=False, store=True)
    country_id_invoice = fields.Many2one(
        'res.country', string='ประเทศ',related='street_invoice.country_id', readonly=False, store=True)
     # Address delivery
    street_delivery = fields.Many2one('res.city.zip','ที่อยู่(เลือก)',tracking=True)
    zip_delivery = fields.Char('รหัสไปรษณี',related='street_delivery.name', tracking=True,change_default=True, compute='_compute_partner_address_values', readonly=False, store=True)
    state_id_delivery = fields.Many2one(
        "res.country.state", string='จังหวัด', related='street_delivery.state_id',tracking=True,readonly=False, store=True)
    country_id_delivery = fields.Many2one(
        'res.country', string='ประเทศ',related='street_delivery.country_id', readonly=False, store=True)

    @api.model
    def get_date_to_convert_name(self, leads):
        val = {
                'company_name' : leads.partner_name,
                'address' : leads.tree.id,
                'post_code' : leads.zip,
                'country_id' : leads.country_id.id,
                'state_id' : leads.state_id,
                'e_mail' : leads.email_from,
                'phone' : leads.phone,
                'user_id' : leads.user_id.id,
                'line_id' : leads.line_id,
                'street_invoice' : leads.street_invoice.id,       
                'zip_invoice' : leads.zip_invoice,     
                'state_id_invoice' : leads.state_id_invoice.id,          
                'country_id_invoice' : leads.country_id_invoice.id,           
                'street_delivery' : leads.street_delivery.id,        
                'zip_delivery' : leads.zip_delivery,      
                'state_id_delivery' : leads.state_id_delivery.id,           
                'country_id_delivery' : leads.country_id_delivery.id,
                'website' : leads.website,
                'Note_address' : leads.Note_address
            }
        organize_id = self.env['customer.organize'].create(val)
        _logger.info(organize_id)
        if leads.contact_name:
            con = {
                    't_name' : leads.title.id,
                    'full_name' : leads.contact_name,
                    'company_id' : organize_id.id, 
                    'e_mail' : leads.email_from, 
                    'phone' : leads.phone, 
                    'user_id' : leads.user_id.id,  
                    'line_id' : leads.line_id,
                    'job_position' : leads.function
                }
            self.env['customer.customers'].create(con)
        
        
   

# ประเภทบริษัท 
class Typedetails(models.Model):
    _name = 'customer.organize.typeor'
    _description = 'Type organize'
    _rec_name = 'name_type'
    name_type = fields.Char()


