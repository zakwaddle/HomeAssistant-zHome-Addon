import React, {useState} from 'react';
import useApi from "../../../../hooks/useApi";
import styled from "styled-components";

const FormContainer = styled.form`
  display: flex;
  flex-direction: column;
  flex: 1 0;
`

const FormLabel = styled.label`
  display: flex;
  justify-content: space-between;
  align-items: center;
`

const AddDeviceForm = ({hideForm}) => {
    const [deviceId, setDeviceId] = useState('');
    const [platform, setPlatform] = useState('');
    const [displayName, setDisplayName] = useState('');

    const {addDevice} = useApi()
    const clearFields = () => {
        setDeviceId('');
        setPlatform('');
        setDisplayName('');
    }

    const handleSubmit = async (event) => {
        event.preventDefault();

        addDevice(deviceId, platform, displayName)
            .then(data => {
                console.log(data);
                if (data && data.success) {
                    clearFields();
                    hideForm()
                }
            })
    };

    return (
        <FormContainer onSubmit={handleSubmit}>
            <FormLabel>
                Device ID
                <input type="text" value={deviceId} onChange={e => setDeviceId(e.target.value)}/>
            </FormLabel>
            <FormLabel>
                Platform
                <input type="text" value={platform} onChange={e => setPlatform(e.target.value)}/>
            </FormLabel>
            <FormLabel>
                Display Name
                <input type="text" value={displayName} onChange={e => setDisplayName(e.target.value)}/>
            </FormLabel>

            <div>
                <button type="submit">Add Device</button>
            </div>
        </FormContainer>
    );
};

export default AddDeviceForm;
