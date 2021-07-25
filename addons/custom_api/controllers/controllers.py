# -*- coding: utf-8 -*-
from odoo import http
import json

from werkzeug.wrappers import Request

class CustomApi(http.Controller):
    @http.route('/api/products/images', auth='user', type='http')
    def index(self, **kw):
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
        data = {'data': data}
        return json.dumps(data)