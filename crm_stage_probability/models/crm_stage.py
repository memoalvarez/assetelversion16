from odoo import fields, models

class CrmStage(models.Model):
    _inherit = "crm.stage"

    probability = fields.Float(
        "Porcentaje (%)",
        required=True,
        default=10.0,
        help="Porcentaje asignado a la etapa",
    )
    on_change = fields.Boolean(
        "Cambiar Porcentaje Por Etapa",
        help="Activar el porcentaje especifico por cada etapa",
    )

    _sql_constraints = [
        (
            "check_probability",
            "check(probability >= 0 and probability <= 100)",
            "El porcentaje debe estar entre 0% y 100%!",
        )
    ]
