# -*- coding: utf-8 -*-
from odoo import http

# class Cotaco(http.Controller):
#     @http.route('/cotaco/cotaco/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cotaco/cotaco/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cotaco.listing', {
#             'root': '/cotaco/cotaco',
#             'objects': http.request.env['cotaco.cotaco'].search([]),
#         })

#     @http.route('/cotaco/cotaco/objects/<model("cotaco.cotaco"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cotaco.object', {
#             'object': obj
#         })