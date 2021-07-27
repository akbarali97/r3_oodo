# -*- coding: utf-8 -*-
from odoo import http
import json

class CustomApi(http.Controller):
    @http.route('/api/auth', type='http', auth="none", csrf=False, methods=['POST'])
    def authenticate(self, db, login, password):
        try:
            http.request.session.authenticate(db, login, password)
        except Exception as e:
            return json.dumps({'status': 'Authentication Failed'})
        data = http.request.env['ir.http'].session_info()
        data = {'session_id': data.get('session_id')}
        return json.dumps(data, indent=4)

    @http.route('/api/products', auth='user', type='http', csrf=False, methods=['GET'])
    def get_products(self, **kw):
        products = http.request.env['product.template'].search([])
        products = products.mapped('name')
        return json.dumps({'data': products}, indent=4)

    @http.route('/api/products/images', auth='user', type='http', csrf=False, methods=['GET'])
    def get_products_images(self, **kw):
        products = http.request.env['product.template'].search([])
        data = list()
        for product in products:
            if product['x_web_images']:
                base_url = http.request.env['ir.config_parameter'].sudo().get_param('web.base.url')
                images_urls = [base_url + image['local_url'] for image in product['x_web_images']]
                data.append({
                    'name': product['name'],
                    'images': images_urls
                })
        return json.dumps({'data': data}, indent=4)