import {configureStore} from '@reduxjs/toolkit'
import {Provider} from "react-redux";
import React from "react"

import {globalStateReducer} from "./globalStateSlice";


const store = configureStore({
    reducer: {
        globalState: globalStateReducer,
    }
})

export const MainProvider = ({children}) => <Provider store={store}>{children}</Provider>

export default store;
