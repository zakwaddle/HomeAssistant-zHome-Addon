import React, {useState} from "react";
import styled from "styled-components";
import {Button} from "../../../../styles/SectionStyles";

const Box = styled.div`
  width: 100%;
`

const Form = styled.form`
  width: 100%;
  display: flex;
  flex-direction: column;
  padding: 1em;
`

const UpdateHostForm = ({submitHandler, cancelHandler}) => {
    const [host, setHome] = useState('')

    const handleSubmit = async (event) => {
        event.preventDefault()
        submitHandler(host)
    }
    return (
        <Box>
            <Form onSubmit={handleSubmit}>
                <label>Host
                    <input type={'text'} value={host} onChange={event => setHome(event.target.value)}/>
                </label>

                <button type={'submit'} style={{display: 'None'}}>submit</button>
            </Form>
            <div>
                <Button onClick={cancelHandler}>Cancel</Button>
                <Button onClick={handleSubmit}>Save</Button>
            </div>
        </Box>

    )

}

export default UpdateHostForm;