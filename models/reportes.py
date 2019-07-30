# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
import logging

_logger = logging.getLogger(__name__)


class Conbranza(models.TransientModel):
    #_name = 'attendance.recap.report.wizard'
    _name = 'cotaco.cobranza.report.wizard'
    #cliente = fields.Many2one(comodel_name="res.partner", string="Cliente", required=True, )
    date_ini = fields.Date(string="Fecha Inicial", required=True, default=fields.Date.today)
    date_end = fields.Date(string="Fecha Final", required=True, default=fields.Date.today)
    informe=fields.Selection([
        (1,'Transportes Realizados'),
        ], 'Tipo de informe', required=False)

    @api.multi
    def get_report(self):
        """Call when button 'Get Report' clicked.
        """
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                #'cliente':self.cliente.id,
                #'nombreCliente':self.cliente.name,
                'date_ini': self.date_ini,
                'date_end': self.date_end,
            },
        }

        # use `module_name.report_id` as reference.
        # `report_action()` will call `get_report_values()` and pass `data` automatically.
        informe=self.env.ref('cotaco.recap_report').report_action(self, data=data)
        return self.env.ref('cotaco.recap_report').report_action(self, data=data)
    @api.multi
    def imprimir_excel(self):
        #r = requests.get('http://localhost:8069/web/binary/download_document?informe=%s&wizard=%s'%(self.informe,int(self.id)), auth=HTTPBasicAuth('admin', 'opendrive1885'))
        #return r
        _logger.info(self)
        _logger.info(self.informe)
        _logger.info(self.id)
        return {
            'type' : 'ir.actions.act_url',
            'url': '/web/get_excel?informe=%s&wizard=%s'% (self.informe, self.id),
            'target': 'self'
        }

class ReportAttendanceRecap(models.AbstractModel):
    """Abstract Model for report template.
    for `_name` model, please use `report.` as prefix then add `module_name.report_name`.
    """
    _name = 'report.cotaco.attendance_recap_report_view'

    @api.model
    def get_report_values(self, docids, data=None):
        totalDeuda=0
        #cliente = data['form']['cliente']
        #nombreCliente=data['form']['nombreCliente']
        date_ini = data['form']['date_ini']
        date_ini_obj = datetime.strptime(date_ini, DATE_FORMAT)

        date_end = data['form']['date_end']
        date_end_obj = datetime.strptime(date_end, DATE_FORMAT)

        docs = []
        facturas = self.env['sale.order'].search([('state','=','sale'),
                                                       #('partner_id','=',cliente),
                                                        ('confirmation_date', '>=', date_ini_obj.strftime(DATETIME_FORMAT)),
                                                       ('confirmation_date','<=',date_end_obj.strftime(DATETIME_FORMAT))])
        totalDeuda= sum(item.amount_total for item in facturas)

        for factura in facturas:
            docs.append({
                'Chofer': factura.tag_ids.name,
                'Patente': factura.order_line.analytic_tag_ids.name,
                'NumeroPedido': factura.name,
                'Fecha':factura.confirmation_date,
                'Saldo': factura.amount_total,
                'Detalle': factura.order_line.name,
                'Cantidad': factura.order_line.qty_invoiced,
                'Valor': factura.order_line.price_subtotal,
            })

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'cliente':'Prueba',
            'nombreCliente':'Prueba',
            'date_end': date_end,
            'docs': docs,
            'totalDeuda':totalDeuda
        }