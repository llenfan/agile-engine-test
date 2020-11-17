import { Form, Button, Alert, FormControl } from 'react-bootstrap'

import { useForm } from 'react-hook-form'
import { useState } from 'react'
import { useRouter } from 'next/router'

import axios from 'axios';

const Home = () => {
  
  const { register, handleSubmit } = useForm();
  const [error, setError] = useState()
  const [isDisabled, setIsDisabled] = useState()
  
  let isLoading = false
  let buttonMessage = 'submit'
  
  const router = useRouter()

  var amount = 0

  const submitForm = () => {
    isLoading = true
    buttonMessage = 'sending...'
    setError();
  }

  const handleAmountChange = e => {
    amount = e.target.value
  }

  const onSubmit = data => {
    
    

    //const router = useRouter()
    //router.push('/transaction/history')
    axios.post("http://localhost:5001/transaction", data)
    .then(res => {
      console.log(res);
      console.log(res.data);
      router.push('/history')      
    }).catch(error => {
      setError(error.message)
      console.error('There was an error!', error);
    })  

  }

  return (
    <>
    <Form onSubmit={ handleSubmit(onSubmit)}>

      <Form.Group controlId="formAccountType">
        <Form.Label>movement type</Form.Label>
        <Form.Check 
          ref={register}
          type="radio"
          name="type" 
          id="radio-credit"
          label="credit" 
          value="credit"
        />
        <Form.Check 
          ref={register}
          type="radio"
          name="type" 
          id="radio-debt"
          label="debt"
          value="debit"
        />
      </Form.Group>

      <Form.Group controlId="formBasicEmail">
        <Form.Label>amount</Form.Label>
        <Form.Control name="amount" placeholder="1.00" onChange={handleAmountChange} ref={register}/>
      </Form.Group>
  
      { error &&
        <Alert variant="danger">
          {error}
        </Alert>
      }
      <Button 
        variant="primary" 
        type="submit"
        disabled={isDisabled} 
      >
        {buttonMessage}
      </Button>
    </Form>
    </>
  )
}

export default Home