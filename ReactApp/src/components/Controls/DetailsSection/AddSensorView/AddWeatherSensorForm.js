import useApi from "../../../../hooks/useApi";
import React, {useState} from "react";
import {FormInput, FormLabel} from "../../../../styles/FormStyles";
import {Button} from "../../../../styles/SectionStyles";
import {AddSensorFormContainer} from "./FormStyles";

const AddWeatherSensorForm = ({deviceConfigId, deviceName, handleCancel, updateDevice}) => {
    // const dispatch = useDispatch()
    const {addSensor} = useApi()
    const [name, setName] = useState('');
    const [pin, setPin] = useState(null);
    const [measurementInterval, setMeasurementInterval] = useState(10000);
    const clearFields = () => {
        setName('')
        setPin(null)
        setMeasurementInterval(10000)
    }
    const handleSubmit = async (event) => {
        event.preventDefault();
        const formattedName = name.toLowerCase().replace(' ', '_')
        const formattedDeviceName = deviceName.toLowerCase().replace(' ', '_')
        const temperatureName = `${formattedName}-temperature`
        const humidityName = `${formattedName}-humidity`
        const baseTopic = `homeassistant/sensor/${formattedDeviceName}`
        const temperatureTopic = `${baseTopic}/${temperatureName}`
        const humidityTopic = `${baseTopic}/${humidityName}`
        addSensor("weather", name, deviceConfigId,
            {
                pin: pin,
                measurement_interval_ms: measurementInterval,
                name_temp: temperatureName,
                name_humidity: humidityName,
                topics: {
                    temperature_topic: temperatureTopic,
                    temperature_discovery: `${temperatureTopic}/config`,
                    humidity_topic: humidityTopic,
                    humidity_discovery: `${humidityTopic}/config`,
                }


            }).then(data => {
            if (data && data.success) {
                clearFields();
                updateDevice();
                handleCancel && handleCancel()
            }
        })
    };
    return (
        <AddSensorFormContainer onSubmit={handleSubmit}>
            <FormLabel>
                Name
                <FormInput type="text" value={name} onChange={e => setName(e.target.value)}/>
            </FormLabel>
            <FormLabel>
                Pin
                <FormInput type="number" value={pin} onChange={e => setPin(Number(e.target.value))}/>
            </FormLabel>
            <FormLabel>
                Measurement Interval (ms)
                <FormInput type="number" value={measurementInterval} onChange={e => setMeasurementInterval(Number(e.target.value))}/>
            </FormLabel>

            <div>
                <Button onClick={handleCancel && handleCancel}>Cancel</Button>
                <Button type="submit">Save</Button>
            </div>
        </AddSensorFormContainer>
    );
}

export default AddWeatherSensorForm;