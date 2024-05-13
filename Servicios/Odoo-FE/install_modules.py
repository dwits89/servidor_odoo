import xmlrpc.client
from time import sleep

# Configuración
url = "http://localhost:8069"
db = "dwits_fe"
username = 'manuel.sanchez@ext.datacontrol.es'
password = 'hm27bq2NZedtg2c'

# Obtiene la información común
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))

# Autentica
uid = common.authenticate(db, username, password, {})

# Obtiene el objeto models
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

# Lista de módulos para instalar, completa con tus módulos
modules_to_install = [
    'sale_management', 'account', 'account_financial_report', 'mail', 'contacts', 'web_responsive',
    'base_address_extended', 'account_asset_management', 'account_banking_mandate', 'account_chart_update',
    'account_due_list', 'account_edi', 'account_edi_ubl_cii', 'account_invoice_overdue_reminder',
    'account_invoice_refund_link', 'account_lock_date_update', 'account_move_name_sequence', 'account_payment',
    'account_payment_invoice_online_payment_patch', 'account_payment_mode', 'account_payment_order',
    'account_payment_partner', 'account_payment_sale', 'account_qr_code_sepa', 'account_reconcile_oca',
    'account_sequence', 'account_statement_base', 'account_statement_import_base', 'account_statement_import_file',
    'account_tax_balance', 'analytic', 'auth_signup', 'auth_totp', 'auth_totp_mail', 'auth_totp_portal',
    'auto_backup', 'barcodes', 'barcodes_gs1_nomenclature', 'base', 'base_bank_from_iban', 'base_iban',
    'base_import', 'base_install_request', 'base_iso3166', 'base_location', 'base_location_geonames_import',
    'base_partner_sequence', 'base_setup', 'base_sparse_field', 'base_technical_features', 'base_vat', 'bus',
    'contract', 'contract_payment_mode', 'date_range', 'date_range_account', 'digest', 'disable_odoo_online',
    'document_url', 'iap', 'iap_mail', 'l10n_es', 'l10n_es_account_asset', 'l10n_es_account_statement_import_n43',
    'l10n_es_aeat', 'l10n_es_aeat_mod115', 'l10n_es_aeat_mod123', 'l10n_es_aeat_mod303', 'l10n_es_aeat_mod347',
    'l10n_es_aeat_mod349', 'l10n_es_aeat_mod390', 'l10n_es_aeat_partner_check', 'l10n_es_dua', 
    'l10n_es_toponyms', 'l10n_es_vat_book', 'mail_bot', 'partner_autocomplete',
    'partner_firstname', 'partner_manual_rank', 'payment', 'portal_rating', 'privacy_lookup', 'product',
    'product_margin', 'rating', 'remove_odoo_enterprise', 'report_qweb_parameter', 'report_xlsx', 'report_xlsx_helper',
    'report_xml', 'resource', 'sale', 'sale_product_configurator', 'sale_product_template_tags', 'sale_sms',
    'sales_team', 'server_action_mass_edit', 'show_db_name', 'sms', 'snailmail', 'snailmail_account', 'social_media',
    'spreadsheet', 'spreadsheet_account', 'spreadsheet_dashboard', 'spreadsheet_dashboard_sale', 'uom', 'utm', 'web',
    'web_editor', 'web_kanban_gauge', 'web_no_bubble', 'web_timeline', 'web_tour', 'web_unsplash', 'gamification',
    'portal', 'http_routing', 'phone_validation'
]






def install_modules(modules_to_install):
    failed_modules = []

    for module in modules_to_install:
        success = False
        for attempt in range(3):  # Reintenta hasta 3 veces
            try:
                # Buscar el módulo por su nombre
                module_id = models.execute_kw(db, uid, password, 'ir.module.module', 'search', [[('name', '=', module)]])
                if module_id:
                    models.execute_kw(db, uid, password, 'ir.module.module', 'button_immediate_install', [module_id])
                    print(f"Módulo {module} instalado con éxito.")
                    success = True
                    break
                else:
                    print(f"Módulo {module} no encontrado.")
                    break
            except Exception as e:
                print(f"Error al instalar el módulo {module}: {str(e)} (Intento {attempt + 1}/3)")
                sleep(5)  # Espera de 5 segundos entre intentos

        if not success:
            failed_modules.append(module)

    return failed_modules

# Intentar instalar los módulos, reintentando los fallidos hasta 3 veces
remaining_modules = modules_to_install
for i in range(3):
    remaining_modules = install_modules(remaining_modules)
    if not remaining_modules:
        break

if remaining_modules:
    print(f"Los siguientes módulos no se pudieron instalar tras 3 intentos: {remaining_modules}")
else:
    print("Todos los módulos solicitados han sido instalados con éxito.")
