import useApi from "../../../../hooks/useApi";
import React, {useState} from "react";
import {FormContainer, FormInput, FormLabel} from "../../../../styles/FormStyles";
import {Button} from "../../../../styles/SectionStyles";
import {AddSensorFormContainer} from "./FormStyles";

const AddButtonForm = ({deviceConfigId, deviceName, handleCancel, updateDevice}) => {
    // const dispatch = useDispatch()
    const {addSensor} = useApi()
    const [name, setName] = useState('');
    const [pin, setPin] = useState(null);
    const [retrigDelay, setRetrigDelay] = useState(300);
    const clearFields = () => {
        setName('')
        setPin(null)
        setRetrigDelay(300)
    }
    const handleSubmit = async (event) => {
        event.preventDefault();
        const formattedName = name.toLowerCase().replace(' ', '_')
        const formattedDeviceName = deviceName.toLowerCase().replace(' ', '_')
        const baseTopic = `homeassistant/button/${formattedDeviceName}/${formattedName}`
        const commandTopic = `${baseTopic}/commands`
        const stateTopic = `${baseTopic}/state`
        const availabilityTopic = `${baseTopic}/availability`
        const discoveryTopic = `${baseTopic}/config`

        addSensor("button", name, deviceConfigId,
            {
                pin: pin,
                retrigger_delay_ms: retrigDelay,
                topics: {
                    command_topic: commandTopic,
                    state_topic: stateTopic,
                    discovery_topic: discoveryTopic,
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
                Pin
                <FormInput type="number" value={pin} onChange={e => setPin(Number(e.target.value))}/>
            </FormLabel>
            {/* <FormLabel>
                Re-Trigger Delay (ms)
                <FormInput type="number" value={retrigDelay} onChange={e => setRetrigDelay(Number(e.target.value))}/>
            </FormLabel> */}

            <div>
                <Button onClick={handleCancel && handleCancel}>Cancel</Button>
                <Button type="submit">Save</Button>
            </div>
        </AddSensorFormContainer>
    );
}

export default AddButtonForm;