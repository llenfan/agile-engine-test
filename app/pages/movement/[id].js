import React from 'react'
import { Card, Button, Table } from 'react-bootstrap'
import { useRouter } from 'next/router'

function Page({ movement }) {
  
  const router = useRouter()

  const handleClick = (e) =>  {
    e.preventDefault()
    router.push('/history')
  }

  return <>
    <br />
    <Card>
  <Card.Header>Movement details</Card.Header>
  <Card.Body>
    <Table responsive>
      <thead>
      </thead>
      <tbody>
        <tr>
          <td>#</td>
          <td>{movement.id}</td>
        </tr>
        <tr>
          <td>type</td>
          <td>{movement.type}</td>
        </tr>
        <tr>
          <td>amount</td>
          <td>{movement.amount}</td>
        </tr>
        <tr>
          <td>effective date</td>
          <td>{movement.effective_date}</td>
        </tr>
      </tbody>
    </Table>
    <Button variant="primary" onClick={handleClick}>history</Button>
  </Card.Body>
</Card>
    </>
}

Page.getInitialProps = async (ctx) => {
  console.log("http://localhost:5001/transaction/" + ctx.query.id)
  console.log(ctx.query.id)
  const res = await fetch("http://localhost:5001/transaction/" + ctx.query.id)
  const movement = await res.json()
  return { movement }
}

export default Page
