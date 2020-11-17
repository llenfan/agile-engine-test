import { Table } from "react-bootstrap";
import Link from 'next/link'
import styles from '../styles/Home.module.css'

const Page = ({ transactions }) => {

  return <>
    <h3 style={{ textAlign: 'center' }}>{ `movements history` }</h3>
    <Table responsive>
      <thead>
        <tr>
          <th>type</th>
          <th>amount</th>
          <th>actions</th>
        </tr>
      </thead>
      <tbody>
      {
          transactions.map((d, idx) => (
              <tr key={idx} className={(d.type == 'credit') ? styles.row_credit : styles.row_debit}>
                  <td>{d.type}</td>
                  <td>{d.amount}</td>
                  <td>
                    <Link href={`/movement/${encodeURIComponent(d.id)}`}>
                      <a>details</a>
                    </Link>
                  </td>
              </tr>
          ))
      }
      </tbody>
  </Table>
  </>

}

Page.getInitialProps = async (ctx) => {
  const res = await fetch('http://localhost:5001/transaction/history')
  const json = await res.json()
  return { transactions: json }
}

export default Page