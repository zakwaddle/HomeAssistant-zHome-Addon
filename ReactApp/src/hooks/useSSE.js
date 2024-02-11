import React from "react";
import {useDispatch} from "react-redux";
import {globalStateActions} from "../store/globalStateSlice";

const config = require('../../zrc')

export default function useSSE() {

    const dispatch = useDispatch()

    React.useEffect(() => {
        const url = `${config.apiHost}/stream`
        console.log(`SSE Stream: ${url}`)

        const eventSource = new EventSource(url);

        eventSource.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.type === 'log') {
                dispatch(globalStateActions.addDeviceLog(data.log))
                dispatch(globalStateActions.updateShouldScroll(true))
            }
            if (data.type === 'device') {
                console.log(data.device)
                if (data.device.displayName === null) {
                    dispatch(globalStateActions.addNewDevice(data.device))
                } else {
                    dispatch(globalStateActions.addDevice(data.device))
                }
            }

        };

        return () => {
            eventSource.close();
        };
    }, []);

}