'''
Created on Sep 1, 2013

@author: phyo936
'''
from openerp import models, fields, api, _
from openerp.exceptions import ValidationError


class doctor(models.Model):
    _name = "clinic.doctor"
    _description = "Clnic Doctor"
    _order = "name"
    
    name =  fields.Char(String ='Doctor Name', size=64, required=True)
    active = fields.Boolean(String ='Active', help="If the active field is set to False, it will allow you to hide the payment term without removing it.",default='1')
    age =    fields.Integer(String ='Age')
    specialist = fields.Char(String ='Specialist')
    address = fields.Text(String ='Address')
    phoneno = fields.Char(String ='Phone No')
    appnum = fields.One2many('clinic.appointment','doctor_id',String='Appointments')
    no_apps = fields.Integer(compute='_num_appointments', string="No. of Appointments")
        
        
    @api.one
    def _num_appointments(self):
        
        for doc in self:
            count = len(doc.appnum)
          
        doc.update({
                'no_apps': count,
            })

    
    

class patient(models.Model):
    _name = "clinic.patient"
    _description = "Patient"

    name = fields.Char(String ='Patient Name', size=64, required=True)
    nrc = fields.Char(String='NRC ID', required=True)
    sex = fields.Selection([('male', 'Male'), ('female', 'Female')], String = 'Gendar',default = 'male')
    age = fields.Integer(String = 'Age')

    _order = "name"
    
     
                           
      
class appointment(models.Model):
    _name = "clinic.appointment"
    _description = "Appointment"
    _rec_name = 'appnum'
    
   
    @api.one
    @api.constrains('age')
    def _check_age(self):
        #for appointment in self:
        if self.age < 8:
            raise ValidationError(_('Patient must be older than 8 years !'))
        return True
   

    appnum = fields.Char(String = 'Appointment Num', readonly=True)
    appdate= fields.Date(String = 'Appointment Date')
    doctor_id = fields.Many2one('clinic.doctor', String = 'Doctor')
    patientname = fields.Char(String = 'Patient Name', required=True)
    patientnrc = fields.Char(String = 'Patient NRC')
    sex = fields.Selection([('male', 'Male'), ('female', 'Female')], String = 'Gender' , default = 'male')
    age = fields.Integer(String = 'Age')
    state = fields.Selection([
                ('book', 'Booked'),
                ('confirm', 'Confirmed'),
                ('cancel', 'Cancelled'),
      ], String = 'States' , default ='book')
    
    
                     
    
 
    _sql_constraints=[('patient_name_uniq', 'unique(patientname,appdate)', 
                                   'Same Patient is already make appointment for same day!' )]
    
#    _constraints = [(_check_age, "Patient must be older than 8 years !", ['age'])]
    
    
    
    @api.one
    def confirm(self):
        #self.write(cursor, user, ids, {'state':'confirm'})
        self.write({'state':'confirm'})
        #saving to patient data.
        #creating obj
        #patient_obj = self.pool.get('clinic.patient')
        patient_obj =  self.env['clinic.patient']
        #appointments = self.browse(cursor, user, ids, context=ctx)
        appointments = self
        appointment = appointments[0];
        value={
                'name' :appointment.patientname,
                'nrc' : appointment.patientnrc,
                'sex' : appointment.sex,
                'age' : appointment.age,
               }
        #orm saving the object by using map
        patient_obj.create(value)
        return True;
    
    @api.one
    def cancel(self):
        #self.write(cursor, user, ids, {'state':'cancel'})
        self.write({'state': 'cancel'})
        #patient_obj = self.pool.get('clinic.patient')
        patient_obj = self.env['clinic.patient']
        #appointments = self.browse(cursor, user, ids, context=context)
        appointments = self
        appointment = appointments[0];
        
        #patient_ids = patient_obj.search(cursor,user,[('name','=',appointment.patientname)])
        #patient_ids = patient_obj.search([('name','=',appointment.patientname)])
        #print patient_ids
        
        #patient_obj.unlink(patient_ids)
        
        patient_obj.search([('name','=',appointment.patientname)]).unlink()
        
        
      
        return True;

    @api.model
    def create(self,vals):
        print vals
        #appointment_num = self.pool.get('ir.sequence').get(cursor, user,
        #    'appointment.code') or '/'
        appointment_num = self.env['ir.sequence'].get('appointment.code') or '/'
        vals['appnum'] = appointment_num
        return super(appointment, self).create(vals)
    
appointment()

class medicine(models.Model):
    
    _name = "product.template"
    _description = "medicine"
    _inherit = "product.template"

    expireDate = fields.Date(String = 'Expire Date')
    code = fields.Char(String ='Medicine Code')
    is_medicine = fields.Boolean(String = 'Medicine')
    
medicine()
