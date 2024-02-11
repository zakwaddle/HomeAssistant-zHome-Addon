import React, {useState} from 'react';
import useApi from "../../../../hooks/useApi";
import styled from "styled-components";
import {FormContainer, FormInput, FormLabel} from "../../../../styles/FormStyles";
import {useDispatch} from "react-redux";
import {globalStateActions} from "../../../../store/globalStateSlice";

// const AddWifiForm = ({addNew, hideForm}) => {
const AddWifiForm = ({handleCancel}) => {
    const [ssid, setSSID] = useState('');
    const [password, setPassword] = useState('');

    const {addWifiNetwork} = useApi()
    const clearFields = () => {
        setSSID('');
        setPassword('');
    }
    const dispatch = useDispatch()
    const handleSubmit = async (event) => {
        event.preventDefault();

        addWifiNetwork(ssid, password)
            .then(data => {
                console.log(data);
                if (data && data.success) {
                    clearFields();
                    dispatch(globalStateActions.updateWifiNetwork(data['wifi_network']))
                    dispatch(globalStateActions.updateShowConnectionForm("None"))
                }
            })
    };

    return (
        <FormContainer onSubmit={handleSubmit}>
            <FormLabel>
                SSID
                <FormInput type="text" value={ssid} onChange={e => setSSID(e.target.value)}/>
            </FormLabel>
            <FormLabel>
                Password
                <FormInput type="password" value={password} onChange={e => setPassword(e.target.value)}/>
            </FormLabel>

            <div>
                <button onClick={handleCancel && handleCancel}>Cancel</button>
                <button type="submit">Save</button>
            </div>
        </FormContainer>
    );
};

export default AddWifiForm;
