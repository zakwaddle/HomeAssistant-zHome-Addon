
class TempOutOfRange(Exception):
    pass

registered_triggers = []

class Sensor:

    def __init__(self, name, entity_id):
        self.name = name
        self.id = entity_id

    def state(self):
        return state.get(self.id)


class Thermostat:
    HEAT = 'heat'
    COOL = 'cool'
    OFF = 'off'

    def __init__(self, thermostat_id):
        self.id = thermostat_id

    def mode(self):
        return state.get(self.id)

    def __set_mode(self, new_mode):
        log.info(f"setting thermostat to '{new_mode}' mode")
        climate.set_hvac_mode(
            entity_id=self.id, 
            hvac_mode=new_mode
            )

    def set_mode_to_cool(self):
        self.__set_mode(self.COOL)
    
    def set_mode_to_heat(self):
        self.__set_mode(self.HEAT)
    
    def turn_off(self):
        self.__set_mode(self.OFF)

    def set_target_temperature(self, new_temperature):
        log.info(f"setting thermostat target temperature to '{new_temperature}'")
        climate.set_temperature(
            entity_id=self.id, 
            temperature=new_temperature
            )

    def action(self):
        return state.get(f"{self.id}.hvac_action")

    def current_temperature(self):
        return int(state.get(f"{self.id}.current_temperature"))

    def target_temperature(self):
        return int(state.get(f"{self.id}.temperature"))


class TempRanger:
    sensor: Sensor = None

    def __init__(self, app_config):
        log.info("initializing TempRanger")
        self.config = app_config
        self.selector_id = app_config['sensor_selector']
        self.sensor_options = self.config['sensor_options']
        self.thermostat = Thermostat(self.config['thermostat'])
        self.selector = Sensor("sensor_selector", self.config['sensor_selector'])
        self.range_top = Sensor("range_top", self.config['range_top'])
        self.range_bottom = Sensor("range_bottom", self.config['range_bottom'])
        self.__setup_sensor()

    def has_selection(self):
        # name = self.__selector_value()
        name = self.selector.state()
        return name in self.sensor_options

    def enabled(self):
        value = state.get(self.config['app_enabled'])
        log.info(f'enabled: {value}')
        return True if value == "on" else False

    def heat_enabled(self):
        value = state.get(self.config['heat_enabled'])
        return True if value == "on" else False

    def cool_enabled(self):
        value = state.get(self.config['cool_enabled'])
        return True if value == "on" else False

    # def __selected_sensor_id(self):
    #     selected = self.selector.state()
    #     if selected != 'None':
    #         selected_id = self.sensor_options[selected]
    #         return selected_id

    def __setup_sensor(self):
        if self.has_selection():
            name = self.selector.state()
            # entity_id = self.__selected_sensor_id()
            entity_id = self.sensor_options[name]
            self.sensor = Sensor(name, entity_id)

    def sensor_value(self):
        # sensor_id = self.__selected_sensor_id()
        if self.sensor is not None:
            return float(self.sensor.state())
    
    def target_temperature_value(self):
        return float(state.get(app_config['target_temperature']))

    def target_range(self):
        return float(self.range_top.state()), float(self.range_bottom.state())

def temperature_ranger(app_config, ranger):
    # ranger = TempRanger(app_config)
    # PLUS_MINUS_RANGE = 0.4
    # HAS_SENSOR = f"{app_config['sensor_selector']} != 'None' or {app_config['sensor_selector']} != 'unknown'"
    # STATUS_NOT_BELOW = f"{app_config['status_indicator']} != 'below'"
    # STATUS_NOT_ABOVE = f"{app_config['status_indicator']} != 'above'"
    # STATUS_NOT_IN_RANGE = f"{app_config['status_indicator']} != 'in range'"
    
    # SELECTED_SENSOR = f"{app_config['sensor_options'][state.get(app_config['sensor_selector'])]}"
    # TEMP_IN_RANGE = f"{app_config['range_bottom']} <= {SELECTED_SENSOR} <= {app_config['range_top']}"
    
    
    task.unique("temperature_ranger")
    thermostat = Thermostat(app_config['thermostat'])


    # def get_selected_target_sensor_name():
    #     return state.get(app_config['sensor_selector'])

    # def get_selected_target_sensor_id():
    #     selected = get_selected_target_sensor_name()
    #     if selected != 'None':
    #         selected_id = app_config['sensor_options'][selected]
    #         return selected_id

    # def get_selected_target_sensor_value():
    #     if get_selected_target_sensor_name() != "None":
    #         return float(state.get(get_selected_target_sensor_id()))

    # def get_target_temperature():
    #     return float(state.get(app_config['target_temperature']))

    # def get_switch_value(switch):
    #     if switch == 'on':
    #         return True 
    #     elif switch == 'off':
    #         return False

    # # mode must be one of ['heat', 'cool', 'off']
    # def set_thermostat_mode(new_mode):
    #     log.info(f"setting thermostat to '{new_mode}' mode")
    #     climate.set_hvac_mode(
    #         entity_id=app_config['thermostat'], 
    #         hvac_mode=new_mode
    #         )


    def set_thermostat_target(new_temperature):
        min_target_temperature = state.get(app_config['min_target_temp'])
        max_target_temperature = state.get(app_config['max_target_temp'])
        in_range = float(min_target_temperature) <= float(new_temperature) <= float(max_target_temperature)
        above_range = float(new_temperature) > float(max_target_temperature)
        below_range = float(new_temperature) < float(min_target_temperature)
        if in_range:
            log.info(f"setting thermostat target temperature to '{new_temperature}'")
            thermostat.set_target_temperature(new_temperature)
            # climate.set_temperature(
            #     entity_id=app_config['thermostat'], 
            #     temperature=new_temperature
            #     )
        elif above_range:
            log.info(f"setting thermostat target temperature to max allowed temp: '{max_target_temperature}'")
            thermostat.set_target_temperature(max_target_temperature)
            # climate.set_temperature(
            #     entity_id=app_config['thermostat'], 
            #     temperature=max_target_temperature
            #     )
        elif below_range:
            log.info(f"setting thermostat target temperature to minimum allowed temp:'{min_target_temperature}'")
            thermostat.set_target_temperature(min_target_temperature)
            # climate.set_temperature(
            #     entity_id=app_config['thermostat'], 
            #     temperature=min_target_temperature
            #     )
        else:
            log.info(f"cannot set target temperature out of range {min_target_temperature}-{max_target_temperature} : {new_temperature}")


    # def get_thermostat_mode():
    #     return state.get(app_config['thermostat'])

    # def get_thermostat_action():
    #     return state.get(f"{app_config['thermostat']}.hvac_action")

    # def get_thermostat_current_temperature():
    #     return int(state.get(f"{app_config['thermostat']}.current_temperature"))

    # def get_thermostat_target_temperature():
    #     return int(state.get(f"{app_config['thermostat']}.temperature"))

    # def get_sensor_temperature():
    #     return float(state.get(app_config['target_sensor']))

    # def get_target_range():
    #     return float(state.get(app_config['range_bottom'])), float(state.get(app_config['range_top']))

    # def has_selected_sensor():
    #     return get_selected_target_sensor_name() != 'None'

    def update_status_indicator(new_status):
        if state.get(app_config['status_indicator']) != new_status:
            state.set(var_name=app_config['status_indicator'], value=new_status)
            

    def kick_on_heat():
        log.info("kicking on the heat")
        hvac_mode = thermostat.mode()
        hvac_current_temperature = thermostat.current_temperature()
        hvac_target_temperature = thermostat.target_temperature()

        if hvac_mode != thermostat.HEAT:
            log.info('thermostat mode is not "heat"')
            return
            # set_thermostat_mode('heat')
            # task.sleep(60)
        if hvac_target_temperature > hvac_current_temperature:
            log.info("target temp already above current temp")
            return
        set_thermostat_target(hvac_current_temperature + 1)


    def kick_on_air():
        log.info("kicking on the A/C")
        hvac_mode = thermostat.mode()
        hvac_current_temperature = thermostat.current_temperature()
        hvac_target_temperature = thermostat.target_temperature()

        if hvac_mode != thermostat.COOL:
            log.info('thermostat mode is not "cool"')
            return
            # set_thermostat_mode('cool')
            # task.sleep(60)
        if hvac_target_temperature < hvac_current_temperature:
            log.info("target temp already below current temp")
            return
        set_thermostat_target(hvac_current_temperature - 1)


    def kick_off_heat():
        log.info("kicking off the heat")
        hvac_current_temperature = thermostat.current_temperature()
        hvac_target_temperature = thermostat.target_temperature()

        if hvac_target_temperature < hvac_current_temperature:
            log.info("target temp already below current temp")
            return
        set_thermostat_target(int(hvac_current_temperature) - 1)


    def kick_off_air():
        log.info("kicking off the A/C")
        hvac_current_temperature = thermostat.current_temperature()
        hvac_target_temperature = thermostat.target_temperature()
        
        if hvac_target_temperature > hvac_target_temperature:
            log.info("target temp already above current temp")
            return
        set_thermostat_target(int(hvac_current_temperature) + 2)


    def get_temperature_status():
        log.info('getting temperature status...')
        # range_bottom, range_top = get_target_range()
        range_bottom, range_top = ranger.target_range()
        # sensor_temperature = get_selected_target_sensor_value()
        sensor_temperature = ranger.sensor_value()
        if range_bottom <= sensor_temperature <= range_top:
            log.info(f"temperature status: 'in range' | {range_bottom} <= {sensor_temperature} <= {range_top}")
            return 'in range'
        if sensor_temperature > range_top:
            log.info(f"temperature status: 'above' | {sensor_temperature} > {range_top}")
            return 'above'
        if sensor_temperature < range_bottom:
            log.info(f"temperature status: 'below' | {sensor_temperature} < {range_bottom}")
            return 'below'


    def log_summary(sensor_temperature=None, temperature_status=None, trigger=None):
        log.info(
            f"""
            has_sensor: {ranger.sensor.name}
            hvac_mode: {ranger.thermostat.mode()} 
            hvac_action: {ranger.thermostat.action()}
            hvac_current_temp: {ranger.thermostat.current_temperature()}
            hvac_target_temp: {ranger.thermostat.target_temperature()}
            sensor temperature: {ranger.sensor.state()}
            temperature status: {temperature_status}
            triggered_by: {trigger}
            """)

    def evaluate_thermostat_temperature(trigger=None):

        task.unique("check_thermostat_temperature", kill_me=True)

        hvac_mode = ranger.thermostat.mode()
        hvac_action = ranger.thermostat.action()
        if not ranger.has_selection():
            log.info("no target sensor selected...exiting temperature evaluation")
            return
        
        # log.info(f'evaluating temperature based on {get_selected_target_sensor_name()} sensor')
        log.info(f'evaluating temperature based on {ranger.sensor.name} sensor')
        # sensor_temperature = get_sensor_temperature()
        # sensor_temperature = get_selected_target_sensor_value()
        sensor_temperature = ranger.sensor_value()

        # enabled = get_switch_value(state.get(app_config['app_enabled']))
        # heat_enabled = get_switch_value(state.get(app_config['heat_enabled']))
        # cool_enabled = get_switch_value(state.get(app_config['cool_enabled']))
        
        enabled = ranger.enabled()
        heat_enabled = ranger.heat_enabled()
        cool_enabled = ranger.cool_enabled()
        temperature_status = get_temperature_status()
        if temperature_status == 'in range':
            update_status_indicator('in range')

        elif temperature_status == 'above':
            update_status_indicator('above')
            if not enabled:
                log.info("temperature is above target range, but use_range is off")
                return
            if cool_enabled and hvac_mode == thermostat.COOL:
                if hvac_action == 'cooling':
                    log.info('A/C is already running')
                else:
                    kick_on_air()
            elif heat_enabled and hvac_mode == thermostat.HEAT:
                kick_off_heat()

        elif temperature_status == 'below':
            update_status_indicator('below')
            if not enabled:
                log.info("temperature is below target range, but use_range is off")
                return
            if heat_enabled and hvac_mode == thermostat.HEAT:
                if hvac_action == 'heating':
                    log.info('heat is already running')
                else:
                    kick_on_heat()
            elif cool_enabled and hvac_mode == thermostat.COOL:
                kick_off_air()

        log_summary(sensor_temperature, temperature_status, trigger)



    STATE_HOLD_TIME = 30


    # @state_trigger(f"{STATUS_NOT_BELOW} and {app_config['sensor_options'][state.get(app_config['sensor_selector'])]} < {app_config['range_bottom']}", state_hold=STATE_HOLD_TIME)
    # @state_trigger(f"{app_config['sensor_options'][state.get(app_config['sensor_selector'])]} < {app_config['range_bottom']}", state_hold=STATE_HOLD_TIME)
    @state_trigger(f"{ranger.sensor.id} < {ranger.range_bottom.id}", state_hold=STATE_HOLD_TIME)
    def below_range_trigger():
        log.info(f"triggered by 'target_sensor_below_range' for {ranger.sensor.name}")
        evaluate_thermostat_temperature(trigger="below_range")


    # @state_trigger(f"{STATUS_NOT_ABOVE} and {app_config['sensor_options'][state.get(app_config['sensor_selector'])]} > {app_config['range_top']}", state_hold=STATE_HOLD_TIME)
    # @state_trigger(f"{app_config['sensor_options'][state.get(app_config['sensor_selector'])]} > {app_config['range_top']}", state_hold=STATE_HOLD_TIME)
    @state_trigger(f"{ranger.sensor.id} > {ranger.range_top.id}", state_hold=STATE_HOLD_TIME)
    def above_range_trigger():
        log.info(f"triggered by 'target_sensor_above_range' for {ranger.sensor.name}")
        evaluate_thermostat_temperature(trigger="above_range")


    # @state_trigger(f"{STATUS_NOT_IN_RANGE} and {app_config['range_bottom']} <= {app_config['sensor_options'][state.get(app_config['sensor_selector'])]} <= {app_config['range_top']}", state_hold=STATE_HOLD_TIME)
    # @state_trigger(f"{app_config['range_bottom']} <= {app_config['sensor_options'][state.get(app_config['sensor_selector'])]} <= {app_config['range_top']}", state_hold=STATE_HOLD_TIME)
    @state_trigger(f"{ranger.range_bottom.id} <= {ranger.sensor.id} <= {ranger.range_top.id}", state_hold=STATE_HOLD_TIME)
    def target_sensor_in_range():
        log.info(f"triggered by 'target_sensor_in_range' for {ranger.sensor.name}")
        evaluate_thermostat_temperature(trigger="in_range")


    @state_trigger(f"{app_config['thermostat']}.hvac_action != 'idle'")
    def thermostat_action_change():
        task.unique("thermo_action_checker")
        hvac_action = thermostat.action()
        log.info(f"{hvac_action} has started")
        # task.wait_until(f"{app_config['thermostat']}.hvac_action == 'idle'")
        task.wait_until(f"{thermostat.id}.hvac_action == 'idle'")
        # sensor_state = get_sensor_temperature()
        # sensor_state = ranger.sensor.state()
        log.info(f"{hvac_action} has stopped. target sensor value: {ranger.sensor.state()}")
        evaluate_thermostat_temperature(trigger="thermostat_action_change")

    # @state_trigger(f"{app_config['thermostat']}.hvac_action")
    # def thermostat_check():
    #     task.unique("thermo_checker")
    #     hvac_action = get_thermostat_action()
    #     log.info(f"thermostat is {hvac_action}")
    #     task.sleep(10)
    #     sensor_state = get_sensor_temperature()
    #     # log.info(f"{hvac_action} has stopped. target sensor value: {sensor_state}")
    #     evaluate_thermostat_temperature(trigger="thermo_check")


    @state_trigger(f"{app_config['target_temperature']}")
    def set_range():
        target = float(state.get(app_config['target_temperature']))
        plus_minus = float(state.get(app_config['range_plus-minus']))
        new_max = round(target + plus_minus, 1)
        new_min = round(target - plus_minus, 1)
        new_cool_on_temp = round(target + plus_minus + 1, 1)
        new_heat_on_temp = round(target - plus_minus - 1, 1)
        # fix this to pull entity_id from config
        input_number.set_value(entity_id="input_number.maximum_temp", value=new_max)
        input_number.set_value(entity_id="input_number.minimum_temp", value=new_min)
        input_number.set_value(entity_id="input_number.turn_on_cool_at", value=new_cool_on_temp)
        input_number.set_value(entity_id="input_number.turn_on_heat_at", value=new_heat_on_temp)
        log.info(f"target temp has changed to '{target}'")
        log.info(f"   setting new range {new_min}-{new_max}")
        log.info(f"   setting heat_on/cool_on range {new_heat_on_temp}-{new_cool_on_temp}")
        evaluate_thermostat_temperature(trigger="range_change")

    @state_trigger(f"{app_config['thermostat']} != 'heat' and {app_config['sensor_options'][state.get(app_config['sensor_selector'])]} < {app_config["turn_on_heat_at"]}", state_hold=60)
    def temperature_below_turn_on_heat_at():
        log.info('temperature is below value of "turn_on_heat_at"')
        # hvac_mode = get_thermostat_mode()
        # hvac_action = get_thermostat_action()
        # enabled = get_switch_value(state.get(app_config['app_enabled']))
        # heat_enabled = get_switch_value(state.get(app_config['heat_enabled']))
        hvac_mode = thermostat.mode()
        hvac_action = thermostat.action()
        
        enabled = ranger.enabled()
        # cool_enabled = ranger.cool_enabled()
        heat_enabled = ranger.heat_enabled()
        if not enabled:
            log.info('app not enabled')
            return
        if hvac_mode == 'cool' and heat_enabled:
            # log.info('this would be setting the mode to "heat"')
            log.info('setting thermostat mode to "heat"')
            # set_thermostat_mode('heat')
            thermostat.set_mode_to_heat()
            task.sleep(60)
            evaluate_thermostat_temperature(trigger="set_mode_to_heat")


    @state_trigger(f"{app_config['thermostat']} != 'cool' and {app_config['sensor_options'][state.get(app_config['sensor_selector'])]} > {app_config["turn_on_cool_at"]}", state_hold=60)
    def temperature_above_turn_on_cool_at():
        log.info('temperature is above value of "turn_on_cool_at"')
        hvac_mode = thermostat.mode()
        hvac_action = thermostat.action()
        # enabled = get_switch_value(state.get(app_config['app_enabled']))
        # cool_enabled = get_switch_value(state.get(app_config['cool_enabled']))
        enabled = ranger.enabled()
        cool_enabled = ranger.cool_enabled()
        if not enabled:
            log.info('app not enabled')
            return
        if hvac_mode == thermostat.HEAT and cool_enabled:
            # log.info('this would be setting the mode to "cool"')
            log.info('setting thermostat mode to "cool"')
            thermostat.set_mode_to_cool()
            # set_thermostat_mode('cool')
            task.sleep(60)
            evaluate_thermostat_temperature(trigger="set_mode_to_cool")


    @state_trigger("input_button.check_temperature")
    def check_temperature_button():
        log.info('manual temperature check triggered by "check temperature" button')
        evaluate_thermostat_temperature(trigger="check_temperature_button")

    # @state_trigger(f"{app_config['sensor_selector']}", state_hold=3)
    # def test_thing():
    #     log.info(f'selected name: {get_selected_target_sensor_name()}  id: {get_selected_target_sensor_id()}  value: {get_selected_target_sensor_value()}')


    # sensor_names = [i for i in app_config['sensor_options']]
    # selected_sensor = state.get(app_config['sensor_selector'])
    if ranger.has_selection():
        registered_triggers.append(above_range_trigger)
        registered_triggers.append(below_range_trigger)
        registered_triggers.append(target_sensor_in_range)
        registered_triggers.append(thermostat_action_change)
        registered_triggers.append(set_range)
        # registered_triggers.append(test_thing)
        registered_triggers.append(check_temperature_button)
        registered_triggers.append(temperature_below_turn_on_heat_at)
        registered_triggers.append(temperature_above_turn_on_cool_at)
        #registered_triggers.append(thermostat_check)
    # log.info(f"registered_triggers: {registered_triggers}")
    evaluate_thermostat_temperature(trigger="init")


def clear_triggers():
    global registered_triggers
    registered_triggers = []

@time_trigger('startup')
@state_trigger(f"{pyscript.config['apps'].get('temperature_ranger')['sensor_selector']}")
def main():
    app_config = pyscript.config['apps'].get('temperature_ranger')
    if app_config is None:
        return
    log.info("main func")
    ranger = TempRanger(app_config)
    log.info(f'main func has selection: {ranger.has_selection()}')
    sensor_names = [i for i in app_config['sensor_options']]
    input_select.set_options(entity_id=app_config['sensor_selector'], options=['None', *sensor_names])
    # selected_sensor = state.get(app_config['sensor_selector'])

    if ranger.has_selection():
        log.info("ranger has selection")
        temperature_ranger(app_config, ranger)
    else:
        clear_triggers()
        log.info(f'cleared triggers: registered_triggers={registered_triggers}')
