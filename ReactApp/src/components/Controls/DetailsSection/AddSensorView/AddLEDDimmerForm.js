import React, {useState} from 'react';
import useApi from "../../../../hooks/useApi";
import {FormInput, FormLabel} from "../../../../styles/FormStyles";
import {Button} from "../../../../styles/SectionStyles";
import {AddSensorFormContainer} from "./FormStyles";


const AddLEDDimmerForm = ({deviceConfigId, deviceName, handleCancel, updateDevice}) => {
    const {addSensor} = useApi()
    const [name, setName] = useState('');
    const [pin, setPin] = useState(null);
    const [freq, setFreq] = useState(300);
    const [fadeTimeMS, setFadeTimeMS] = useState(4);
    const [brightnessScale, setBrightnessScale] = useState(255);
    const clearFields = () => {
        setName('')
        setPin(null)
        setFreq(300)
        setFadeTimeMS(4)
        setBrightnessScale(255)
    }
    const handleSubmit = async (event) => {
        event.preventDefault();
        const formattedName = name.toLowerCase().replace(' ', '_')
        const formattedDeviceName = deviceName.toLowerCase().replace(' ', '_')
        const topic = `homeassistant/light/${formattedDeviceName}/${formattedName}`
        const discoveryTopic = `${topic}/config`
        const stateTopic = `${topic}/state`
        const commandTopic = `${topic}/set`
        const brightnessStateTopic = `${topic}/dim/state`
        const brightnessCommandTopic = `${topic}/dim/set`

        addSensor("led", name, deviceConfigId,
            {
                pin: pin,
                freq: freq,
                fade_time_ms: fadeTimeMS,
                brightness_scale: brightnessScale,
                topics: {
                    discovery_topic: discoveryTopic,
                    state_topic: stateTopic,
                    command_topic: commandTopic,
                    brightness_state_topic: brightnessStateTopic,
                    brightness_command_topic: brightnessCommandTopic
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
                Frequency
                <FormInput type="number" value={freq} onChange={e => setFreq(Number(e.target.value))}/>
            </FormLabel>
            <FormLabel>
                Fade Time (ms)
                <FormInput type="number" value={fadeTimeMS} onChange={e => setFadeTimeMS(Number(e.target.value))}/>
            </FormLabel>
            <FormLabel>
                Brightness Scale
                <FormInput type="number" value={brightnessScale}
                           onChange={e => setBrightnessScale(Number(e.target.value))}/>
            </FormLabel>

            <div>
                <Button onClick={handleCancel && handleCancel}>Cancel</Button>
                <Button type="submit">Save</Button>
            </div>
        </AddSensorFormContainer>
    );
}

export default AddLEDDimmerForm;