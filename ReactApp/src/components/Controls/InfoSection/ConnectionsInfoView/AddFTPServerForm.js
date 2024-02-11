import React, {useState} from 'react';
import useApi from "../../../../hooks/useApi";
import {FormContainer, FormInput, FormLabel} from "../../../../styles/FormStyles";
import {useDispatch} from "react-redux";
import {globalStateActions} from "../../../../store/globalStateSlice";


const AddFTPServerForm = ({handleCancel}) => {
    const dispatch = useDispatch()
    const {addFtpServer} = useApi()

    const [hostAddress, setHostAddress] = useState('');
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const clearFields = () => {
        setHostAddress('');
        setUsername('');
        setPassword('');
    }

    const handleSubmit = async (event) => {
        event.preventDefault();

        addFtpServer(hostAddress, username, password)
            .then(data => {
                console.log(data);
                if (data && data.success) {
                    clearFields();
                    dispatch(globalStateActions.updateFtpServer(data['ftp_server']))
                    dispatch(globalStateActions.updateShowConnectionForm("None"))
                    // hideForm()
                }
            })
    };

    return (
        <FormContainer onSubmit={handleSubmit}>
            <FormLabel>
                Host Address
                <FormInput type="text" value={hostAddress} onChange={e => setHostAddress(e.target.value)}/>
            </FormLabel>
            <FormLabel>
                Username
                <FormInput type="text" value={username} onChange={e => setUsername(e.target.value)}/>
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

export default AddFTPServerForm;
