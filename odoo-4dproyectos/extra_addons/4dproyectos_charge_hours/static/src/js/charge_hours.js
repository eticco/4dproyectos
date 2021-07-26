/* Global jscolor */
odoo.define('4dproyectos_charge_hours.charge_hours', function(require) {
    "use strict";

    var basic_controller = require('web.BasicController');
    var config = require('web.config');
    
    basic_controller.include({
    	
    	_applyChanges: function (dataPointID, changes, event) {
        	// Llamada a la función original
        	var super_data = this._super(dataPointID, changes, event);
        	var self = this;
        	this.callCustomFunction;
        	
        	if (this.modelName == "charge.hours.wizard") {
        		var employee = $('input[name="employee_text"]') .val();
        		var production = $('input[name="production_text"]') .val();
        		var workorder = $('input[name="workorder_text"]') .val();
        		// Borrar el timeout
        		clearTimeout(this.callCustomFunction);
        		
        		 var def = this._rpc({
                     model: 'ir.config_parameter',
                     method: 'get_param',
                     args: ["CARGA_HORAS_TIEMPO_COMPROBACION"]
                 }).then(function (time_seconds) {
                	
                	 if (time_seconds == false) {
                		 time_seconds = 2
                	 }
                	 
                	 var time_milliseconds = time_seconds * 1000;
                	 if (employee != undefined && employee != ""
             			&& production != undefined && production != ""
             			&& workorder != undefined && workorder != "") {
             			var chargeHoursButton = $('button[name="action_charge_hours"]')
             			// timeout: Si pasan X segundos desde que llegamos aquí llamar a la función
             			self.callCustomFunction = setTimeout(function(){ chargeHoursButton.click() }, time_milliseconds);
             		}
                 });
        		
        	}

        	return super_data
        },
    	
    });
    
});
