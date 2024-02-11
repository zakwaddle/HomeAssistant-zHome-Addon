import React, {useState} from "react";
import styled from "styled-components";
import {useDispatch, useSelector} from "react-redux";
import {Button} from "../../../../styles/SectionStyles";
import {globalStateActions} from "../../../../store/globalStateSlice";
import SensorCard from "./SensorCard";
import useApi from "../../../../hooks/useApi";

const Row = styled.div`
  width: available;
  display: flex;
  justify-content: space-around;
`

const SensorSection = styled.div`
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
`
const SensorRow = styled.div`
  width: 100%;
  display: flex;
  margin: .5em;

`
const SectionContainer = styled.div`
  display: flex;
  flex-direction: ${props => props['direction'] === 'row' ? 'row' : 'column'};
  padding: .5em;
  margin: .5em;
  width: 100%;
`

const DeviceTitle = styled.h1`
  margin: .25em 0 .5em 1.5em;
`
const Box = styled.div`

  width: 100%;
  height: 100%;

  display: flex;
  flex-direction: column;
  justify-content: space-between;

`
const Property = styled.div`
  display: flex;
  justify-content: space-between;
  margin-left: 2em;
  margin-right: 2em;
  @media (max-width: 700px) {
    flex-direction: row;
  }
`
const PropertyTitle = styled.div`
  margin-left: 2em;
  font-weight: bold;
  @media (max-width: 700px) {
    margin-left: 1em;
  }
`
const PropertyValue = styled.div`
  margin-right: 2em;
  @media (max-width: 700px) {
    margin-right: 1em;
  }
`

const HalfColumn = styled.div`
  display: flex;
  flex-direction: column;
  width: 50%;
`

const Form = styled.form`
  display: flex;
  flex-direction: column;
  justify-content: space-between;
`
const FormLabel = styled.form`
  display: flex;
  justify-content: space-between;
`

const ConfirmContainer = styled.div`
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
`
const DeviceDetailsView = () => {
    const selectedDevice = useSelector(state => state['globalState']['selectedDevice'])
    const config = selectedDevice.config
    const deviceSettings = config["device_settings"]

    const [usePing, setUsePing] = useState(true)
    const [ledOn, setLedOn] = useState(true)
    const [showDeleteScreen, setShowDeleteScreen] = useState(false)
    const [showRenameScreen, setShowRenameScreen] = useState(false)
    const [newName, setNewName] = useState('')

    const showDeleteConfirm = () => setShowDeleteScreen(true)
    const hideDeleteConfirm = () => setShowDeleteScreen(false)
    const showRenameConfirm = () => setShowRenameScreen(true)
    const hideRenameConfirm = () => setShowRenameScreen(false)

    const {deleteDeviceConfig, deleteDevice, sendMessage} = useApi()

    const {device_id, sensors, wifi_network, ftp_server, mqtt_broker} = config
    // const wifi = config['wifi_network']
    // const ftp = config['ftp_server']
    // const mqtt = config['mqtt_broker']
    const dispatch = useDispatch()
    const showSaveButton = !deviceSettings || (deviceSettings['led_on_after_connect'] !== ledOn || deviceSettings['use_ping'] !== usePing)

    React.useEffect(() => {
        if (deviceSettings) {
            if (deviceSettings['use_ping'] !== undefined) {
                setUsePing(deviceSettings['use_ping'])
            }
            if (deviceSettings['led_on_after_connect'] !== undefined) {
                setLedOn(deviceSettings['led_on_after_connect'])
            }
        }
    }, [selectedDevice, config])

    const handleDelete = () => {

        const handleCleanUp = () => {
            dispatch(globalStateActions.updateShouldUpdateDevices(true))
            dispatch(globalStateActions.updateSelectedDevice(null))
        }
        deleteDeviceConfig(device_id)
            .then(data => {
                data && data.success && deleteDevice(device_id)
                    .then(data => {
                        data && data.success && handleCleanUp()
                    })
            })
    }

    const addSensorView = () => dispatch(globalStateActions.updateDetailsSectionView('addSensor'))
    const updateHostView = () => dispatch(globalStateActions.updateDetailsSectionView('updateHost'))
    const {restartDevice, updateDeviceSettings, updateDeviceName} = useApi()
    const handleRestartClick = () => {
        restartDevice(device_id).then(data => console.log(data))
    }
    const handleUpdateSettings = () => {
        updateDeviceSettings(device_id, {'use_ping': usePing, 'led_on_after_connect': ledOn})
            .then(data => console.log(data))
    }
    const handleUpdateName = () => {
        const handleCleanUp = () => {
            dispatch(globalStateActions.updateShouldUpdateDevices(true))
            hideRenameConfirm()
        }
        updateDeviceName(device_id, newName)
            .then(data => {
                data && data.success && handleCleanUp()
            })
    }

    const handleUpdate = () => sendMessage(device_id, {
        "command": "update",
        "manifest_path": "upload/Firmware/manifest.json"
    }).then(data => console.log(data))

    if (showDeleteScreen) {
        return (
            <ConfirmContainer>
                <h2>Delete {selectedDevice['display_name']}?</h2>
                <p>This will delete both the device and device configuration</p>
                <br/>
                <Row>
                    <Button onClick={hideDeleteConfirm}>Cancel</Button>
                    <Button onClick={handleDelete}>Delete</Button>
                </Row>
            </ConfirmContainer>
        )
    }
    if (showRenameScreen) {
        return (
            <ConfirmContainer>
                <h2>Rename {selectedDevice['display_name']}</h2>
                <br/>
                <Form onSubmit={handleUpdateName}>
                    <FormLabel>New Name
                        <input type={'text'}
                               value={newName}
                               onChange={event => setNewName(event.target.value)}/>
                    </FormLabel>

                    <button type={'submit'} style={{display: 'None'}}>submit</button>
                </Form>
                <Row>
                    <Button onClick={hideRenameConfirm}>Cancel</Button>
                    <Button onClick={handleUpdateName}>Rename</Button>
                </Row>
            </ConfirmContainer>
        )
    }

    return (
        <Box>
            <DeviceTitle>{selectedDevice['display_name']}</DeviceTitle>
            <Row>
                <div><Button onClick={showRenameConfirm}>Update Name</Button></div>
                <div><Button onClick={updateHostView}>Update Host</Button></div>
                <div><Button onClick={handleUpdate}>Update</Button></div>
            </Row>
            <SectionContainer>
                <h4>Device Details:</h4>
                <Property>
                    <PropertyTitle>Name</PropertyTitle>
                    <PropertyValue>{selectedDevice['display_name']}</PropertyValue>
                </Property>
                <Property>
                    <PropertyTitle>DeviceID</PropertyTitle>
                    <PropertyValue>{config['device_id']}</PropertyValue>
                </Property>
                <Property>
                    <PropertyTitle>ConfigID</PropertyTitle>
                    <PropertyValue>{config.id}</PropertyValue>
                </Property>
                <Property>
                    <PropertyTitle>Platform</PropertyTitle>
                    <PropertyValue>{selectedDevice['platform']}</PropertyValue>
                </Property>

            </SectionContainer>

            <Row>
                <div><Button onClick={handleRestartClick}>Restart Device</Button></div>
                <div><Button onClick={showDeleteConfirm}>Delete Device</Button></div>
            </Row>

            <SectionContainer direction={'row'}>
                <HalfColumn>
                    <Form onSubmit={handleUpdateSettings}>
                        <FormLabel>Use Ping
                            <input type={'checkbox'}
                                   checked={usePing}
                                   onChange={event => setUsePing(event.target.checked)}/>
                        </FormLabel>
                        <FormLabel>LED On After Connect
                            <input type={'checkbox'}
                                   checked={ledOn}
                                   onChange={event => setLedOn(event.target.checked)}/>
                        </FormLabel>
                        <button type={'submit'} style={{display: 'None'}}>submit</button>
                    </Form>
                </HalfColumn>
                <HalfColumn>
                    <ConfirmContainer>
                        {showSaveButton && <Button onClick={handleUpdateSettings}>Save Settings</Button>}
                    </ConfirmContainer>
                </HalfColumn>
            </SectionContainer>

            <SectionContainer>
                <h4>Connections:</h4>
                <Property>
                    <PropertyTitle>Wifi Network</PropertyTitle>
                    <PropertyValue>{wifi_network && wifi_network.ssid}</PropertyValue>
                </Property>
                <Property>
                    <PropertyTitle>MQTT Broker</PropertyTitle>
                    <PropertyValue>{mqtt_broker && mqtt_broker.host_address}</PropertyValue>
                </Property>
                <Property>
                    <PropertyTitle>FTP Server</PropertyTitle>
                    <PropertyValue>{ftp_server && ftp_server.host_address}</PropertyValue>
                </Property>
            </SectionContainer>

            <SectionContainer>

                <h4>Sensors:</h4>
                <SensorSection>
                    <SensorRow>
                        {sensors.map(sensor => <SensorCard sensorDetails={sensor}/>)}
                    </SensorRow>
                    <Button onClick={addSensorView}>Add Sensor</Button>
                </SensorSection>
            </SectionContainer>

        </Box>
    )
}

export default DeviceDetailsView;