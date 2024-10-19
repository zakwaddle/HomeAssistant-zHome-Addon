import React, {useState} from 'react';
import useApi from "../../../../hooks/useApi";
import {FormInput, FormLabel} from "../../../../styles/FormStyles";
import {Button} from "../../../../styles/SectionStyles";
import {AddSensorFormContainer} from "./FormStyles";


const AddFanForm = ({deviceConfigId, deviceName, handleCancel, updateDevice}) => {
    const {addSensor} = useApi()
    const [name, setName] = useState('');
    const [pin, setPin] = useState(null);
    const [enablePin, setEnablePin] = useState(null);
    const [freq, setFreq] = useState(30000);
    const clearFields = () => {
        setName('')
        setPin(null)
        setEnablePin(null)
        setFreq(30000)
    }
    const handleSubmit = async (event) => {
        event.preventDefault();
        const formattedName = name.toLowerCase().replace(' ', '_')
        const formattedDeviceName = deviceName.toLowerCase().replace(' ', '_')
        const topic = `homeassistant/fan/${formattedDeviceName}/${formattedName}`
        const discoveryTopic = `${topic}/config`
        const availabilityTopic = `${topic}/availability`
        const stateTopic = `${topic}/state`
        const commandTopic = `${topic}/set`
        const percentageStateTopic = `${topic}/dim/state`
        const percentageCommandTopic = `${topic}/dim/set`

        addSensor("fan", name, deviceConfigId,
            {
                pin: pin,
                enable_pin: enablePin,
                freq: freq,
                topics: {
                    discovery_topic: discoveryTopic,
                    state_topic: stateTopic,
                    command_topic: commandTopic,
                    percentage_state_topic: percentageStateTopic,
                    percentage_command_topic: percentageCommandTopic,
                    availability_topic: availabilityTopic
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
                PWM Pin
                <FormInput type="number" value={pin} onChange={e => setPin(Number(e.target.value))}/>
            </FormLabel>
            <FormLabel>
                Enable Pin
                <FormInput type="number" value={enablePin} onChange={e => setEnablePin(Number(e.target.value))}/>
            </FormLabel>
            <FormLabel>
                Frequency
                <FormInput type="number" value={freq} onChange={e => setFreq(Number(e.target.value))}/>
            </FormLabel>

            <div>
                <Button onClick={handleCancel && handleCancel}>Cancel</Button>
                <Button type="submit">Save</Button>
            </div>
        </AddSensorFormContainer>
    );
}

export default AddFanForm;