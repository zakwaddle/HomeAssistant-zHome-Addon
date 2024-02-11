import {useDispatch, useSelector} from "react-redux";
import {globalStateActions} from "../../../../store/globalStateSlice";
import React from "react";
import {Button, CenteredRow, Section, SectionTitle} from "../../../../styles/SectionStyles";
import AddMQTTBrokerForm from "./AddMQTTBrokerForm";
import AddWifiForm from "./AddWifiForm";
import AddFTPServerForm from "./AddFTPServerForm";
import {Property} from "../../../UI/Property";

const WifiSection = ({wifi}) => {
    const dispatch = useDispatch()
    const handleClick = () => dispatch(globalStateActions.updateShowConnectionForm("WIFI"))
    if (!wifi) {
        return (
            <Section>
                <SectionTitle>Wifi Network</SectionTitle>
                <CenteredRow>
                    <div>
                        <Button onClick={handleClick}>Configure Wifi</Button>
                    </div>
                </CenteredRow>
            </Section>
        )
    }
    return (
        <Section>
            <SectionTitle>Wifi Network</SectionTitle>
            <Property name={'ssid'} value={(wifi ? wifi.ssid : '')}/>
            <Property name={'password'} value={(wifi ? wifi.password : '')}/>
        </Section>
    )
}
const MQTTSection = ({mqtt}) => {
    const dispatch = useDispatch()
    const handleClick = () => dispatch(globalStateActions.updateShowConnectionForm("MQTT"))
    if (!mqtt) {
        return (
            <Section>
                <SectionTitle>MQTT Broker</SectionTitle>
                <CenteredRow>
                    <div>
                        <Button onClick={handleClick}>Configure MQTT</Button>
                    </div>
                </CenteredRow>
            </Section>
        )
    }
    return (
        <Section>
            <SectionTitle>MQTT Broker</SectionTitle>
            <Property name={'host'} value={(mqtt ? mqtt.host_address : '')}/>
            <Property name={'port'} value={(mqtt ? mqtt.port : '')}/>
            <Property name={'username'} value={(mqtt ? mqtt.username : '')}/>
            <Property name={'password'} value={(mqtt ? mqtt.password : '')}/>
        </Section>
    )
}
const FTPSection = ({ftp}) => {
    const dispatch = useDispatch()
    const handleClick = () => dispatch(globalStateActions.updateShowConnectionForm("FTP"))
    if (!ftp) {
        return (
            <Section>
                <SectionTitle>FTP Server</SectionTitle>
                <CenteredRow>
                    <div>
                        <Button onClick={handleClick}>Configure FTP</Button>
                    </div>
                </CenteredRow>
            </Section>
        )
    }
    return (
        <Section>
            <SectionTitle>FTP Server</SectionTitle>
            <Property name={'host'} value={(ftp ? ftp.host_address : '')}/>
            <Property name={'username'} value={(ftp ? ftp.username : '')}/>
            <Property name={'password'} value={(ftp ? ftp.password : '')}/>
        </Section>
    )
}


const Wrapper = ({children}) => {
    return ([...children])
}
const ConnectionSection = () => {
    const dispatch =  useDispatch()
    const wifi = useSelector(state => state['globalState']['wifiNetwork'])
    const ftp = useSelector(state => state['globalState']['ftpServer'])
    const mqtt = useSelector(state => state['globalState']['mqttBroker'])
    const connectionKey = useSelector(state => state['globalState']['showConnectionForm'])
    const handleCancel = () => dispatch(globalStateActions.updateShowConnectionForm('None'))

    if (connectionKey === 'None') {
        return (
            <Wrapper>
                <WifiSection wifi={wifi}/>
                <MQTTSection mqtt={mqtt}/>
                <FTPSection ftp={ftp}/>
            </Wrapper>
        )
    }
    if (connectionKey === 'MQTT') {
        return (
            <Wrapper>
                <SectionTitle>MQTT Broker</SectionTitle>
                <AddMQTTBrokerForm handleCancel={handleCancel}/>
            </Wrapper>
        )
    }
    if (connectionKey === 'WIFI') {
        return (
            <Wrapper>
                <SectionTitle>Wifi Network</SectionTitle>
                <AddWifiForm handleCancel={handleCancel}/>
            </Wrapper>
        )
    }
    if (connectionKey === 'FTP') {
        return (
            <Wrapper>
                <SectionTitle>FTP Server</SectionTitle>
                <AddFTPServerForm handleCancel={handleCancel}/>
            </Wrapper>
        )
    }
}

export default ConnectionSection;
