import {createSlice} from "@reduxjs/toolkit";

const initialState = {

    devices: [],
    newDevices: [],
    deviceConfigs: [],
    deviceSensors: [],
    deviceLogs: [],
    wifiNetwork: null,
    ftpServer: null,
    mqttBroker: null,
    shouldScroll: true,
    menuSelection: 'Logs',
    detailsSectionView: 'main',
    selectedDevice: null,
    selectedSensor: null,
    showConnectionForm: 'None',
    shouldUpdateDevices: true

}
const globalStateSlice = createSlice({
    name: 'globalState',
    initialState,
    reducers: {

        updateDevices(state, action) {
            state.devices = action.payload
        },
        updateNewDevices(state, action) {
            state.newDevices = action.payload
        },
        addDevice(state, action){
            state.devices = [...state.devices, action.payload]
        },
        addNewDevice(state, action){
            state.newDevices = [...state.newDevices, action.payload]
        },
        updateDeviceConfigs(state, action) {
            state.deviceConfigs = action.payload
        },
        updateDeviceSensors(state, action) {
            state.deviceSensors = action.payload
        },
        updateDeviceLogs(state, action) {
            state.deviceLogs = action.payload
        },
        addDeviceLog(state, action){
            state.deviceLogs = [...state.deviceLogs, action.payload]
        },
        deleteDeviceLog(state, action){
            const entryID = action.payload
            state.deviceLogs = state.deviceLogs.filter(entry => entry.id !== entryID)
        },
        updateWifiNetwork(state, action) {
            state.wifiNetwork = action.payload
        },
        updateFtpServer(state, action) {
            state.ftpServer = action.payload
        },
        updateMqttBroker(state, action) {
            state.mqttBroker = action.payload
        },
        updateShouldScroll(state, action) {
            state.shouldScroll = action.payload
        },
        updateMenuSelection(state, action) {
            state.menuSelection = action.payload
        },
        updateShowConnectionForm(state, action) {
            state.showConnectionForm = action.payload
        },
        updateSelectedDevice(state, action) {
            state.selectedDevice = action.payload
        },
        updateSelectedSensor(state, action) {
            state.selectedSensor = action.payload
        },
        updateDetailsSectionView(state, action) {
            state.detailsSectionView = action.payload
        },
        updateShouldUpdateDevices(state, action) {
            state.shouldUpdateDevices = action.payload
        },
    }
})

export const globalStateReducer = globalStateSlice.reducer
export const globalStateActions = globalStateSlice.actions