import React, {useState} from "react";
import styled from "styled-components";
import {Button} from "../../../../styles/SectionStyles";
import {globalStateActions} from "../../../../store/globalStateSlice";
import {useDispatch, useSelector} from "react-redux";
import useApi from "../../../../hooks/useApi";
import {Property, PropStack} from "../../../UI/Property";

const SensorDetailsContainer = styled.div`
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-around;

`
const Header = styled.div`
  padding: .5em;
  margin-left: 5%;
`
const ConfigSection = styled.div`
  margin: .25em;
`
const ButtonRow = styled.div`
  width: 100%;
  display: flex;
  position: relative; // Add relative positioning here
  justify-content: flex-start; // Align items to the start
  margin-top: 1em;
`
const LeftButtons = styled.div`
  display: flex;
  //justify-self: flex-start;
`
const CenterButtons = styled.div`
  position: absolute; // Add absolute positioning here
  left: 50%; // Center the div
  transform: translateX(-50%); // Ensure it's centered regardless of its width
`
const DeleteConfirmContainer = styled.div`
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
`
const TopicStack = styled.div`
  width: 100%;
  display: flex;
  flex-direction: column;
  padding: .5em;
`
const TopicLabel = styled.div`
  font-weight: bold;
`
const TopicValue = styled.div`
  //width: 100%;
  //display: flex;
  //justify-content: flex-end;
`

const SensorDetails = () => {
    const [showDeleteConfirm, setShowDeleteConfirm] = useState(false)
    const dispatch = useDispatch()
    const selectedSensor = useSelector(state => state['globalState']['selectedSensor'])
    console.table(selectedSensor)
    const sensorConfig = selectedSensor.sensor_config
    const setDetailsView = () => dispatch(globalStateActions.updateDetailsSectionView('main'))
    const {deleteSensor} = useApi()

    const openDeleteConfirm = () => setShowDeleteConfirm(true)
    const closeDeleteConfirm = () => setShowDeleteConfirm(false)

    const handleDelete = () => {
        deleteSensor(selectedSensor.id)
            .then(() => {
                dispatch(globalStateActions.updateShouldUpdateDevices(true))
                setDetailsView()
            })
    }

    if (showDeleteConfirm) {
        return (
            <DeleteConfirmContainer>
                <h2>Delete {selectedSensor.name}?</h2>
                <br/>
                <ButtonRow>
                    <Button onClick={closeDeleteConfirm}>Cancel</Button>
                    <Button onClick={handleDelete}>Delete</Button>
                </ButtonRow>
            </DeleteConfirmContainer>
        )
    }

    const allConfigKeys = Object.keys(sensorConfig)
    const topicKeys = Object.keys(sensorConfig.topics)
    const configKeys = allConfigKeys.filter(i => i !== 'topics')
    console.log(configKeys)
    return (
        <SensorDetailsContainer>
            <Header>
                <h3>{selectedSensor.name}</h3>
                <h4>type: {selectedSensor.sensor_type}</h4>
            </Header>
            <ConfigSection>
                <h4>Sensor Configs</h4>
                {configKeys.map(k => {
                    return <Property key={k} name={k} value={sensorConfig[k]}/>
                })}
            </ConfigSection>
            <ConfigSection>
                <h4>Sensor Topics</h4>
                {topicKeys.map(k => {
                    // return <Property key={k} name={k} value={sensorConfig.topics[k]}/>
                    return (
                        <TopicStack key={k}>
                            <TopicLabel>{k}</TopicLabel>
                            <TopicValue>{sensorConfig.topics[k]}</TopicValue>
                        </TopicStack>
                    )
                })}
            </ConfigSection>
            <ButtonRow>
                <LeftButtons>
                    <Button onClick={setDetailsView}>Back</Button>
                </LeftButtons>
                <CenterButtons>
                    <Button onClick={openDeleteConfirm}>Delete</Button>
                </CenterButtons>
            </ButtonRow>
        </SensorDetailsContainer>
    )
}

export default SensorDetails;