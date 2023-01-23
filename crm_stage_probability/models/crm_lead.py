from odoo import api, fields, models

class CrmLead(models.Model):
    _inherit = "crm.lead"

    @api.model
    def _onchange_stage_id_values(self, stage_id):
        """ returns the new values when stage_id has changed """
        if not stage_id:
            return {}
        stage = self.env["crm.stage"].browse(stage_id)
        if stage.on_change:
            return {"probability": stage.probability}
        return {}

    @api.onchange("stage_id")
    def _onchange_stage_id(self):
        res = super()._onchange_stage_id()
        values = self._onchange_stage_id_values(self.stage_id.id)
        self.update(values)
        return res

    
