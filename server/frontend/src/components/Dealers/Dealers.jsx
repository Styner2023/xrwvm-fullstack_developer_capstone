import React, { useState, useEffect, useCallback } from 'react'; // Import useCallback
// import React, { useState, useEffect } from 'react';
import "./Dealers.css";
import "../assets/style.css";
import Header from '../Header/Header';
import review_icon from "../assets/reviewicon.png";
import DealershipDatabase from "../data/dealerships.json";

const Dealers = () => {
  const [dealersList, setDealersList] = useState([]);
  const DealersList = DealershipDatabase.dealerships;
  let [states, setStates] = useState([])

  let dealer_url ="/djangoapp/get_dealers";
  
  let dealer_url_by_state = "/djangoapp/get_dealers/";
 
  const filterDealers = async (state) => {
    let dealer_url_by_state = "/djangoapp/get_dealers/";
    if (state === "All") {
      get_dealers();
    } else {
      dealer_url_by_state = dealer_url_by_state+state;
      const res = await fetch(dealer_url_by_state, {
        method: "GET"
      });
      const retobj = await res.json();
      if(retobj.status === 200) {
        let state_dealers = Array.from(retobj.dealers)
        setDealersList(state_dealers)
      }
    }
  }
    const get_dealers = useCallback(async () => { // Wrap get_dealers with useCallback
      const res = await fetch(dealer_url, {
        method: "GET"
      });
      const retobj = await res.json();
      if(retobj.status === 200) {
        let all_dealers = Array.from(retobj.dealers)
        let states = [];
        all_dealers.forEach((dealer)=>{
          states.push(dealer.state)
        });
  
        setStates(Array.from(new Set(states)))
        setDealersList(all_dealers)
      }
    }, []); // Empty dependency array because get_dealers doesn't depend on any state or props
  
    useEffect(() => {
      get_dealers();
    }, [get_dealers]); // Include get_dealers in the dependency array

let isLoggedIn = sessionStorage.getItem("username") != null ? true : false;
return(
  <div>
      <Header/>

     <table className='table'>
      <tr>
      <th>ID</th>
      <th>Dealer Name</th>
      <th>City</th>
      <th>Address</th>
      <th>Zip</th>
      <th>
      <select name="state" id="state" onChange={(e) => filterDealers(e.target.value)}>
      <option value="" selected disabled hidden>State</option>
      <option value="All">All States</option>
      {states.map(state => (
          <option value={state}>{state}</option>
      ))}
      </select>        

      </th>
      {isLoggedIn ? (
          <th>Review Dealer</th>
         ):<></>
      }
      </tr>
     {DealersList.map(dealer => (
        <tr key={dealer.id}>
          <td>{dealer['id']}</td>
          <td><a href={'/dealer/'+dealer['id']}>{dealer['full_name']}</a></td>
          <td>{dealer['city']}</td>
          <td>{dealer['address']}</td>
          <td>{dealer['zip']}</td>
          <td>{dealer['state']}</td>
          {isLoggedIn ? (
            <td><a href={`/postreview/${dealer['id']}`}><img src={review_icon} className="review_icon" alt="Post Review"/></a></td>
           ):<></>
          }
          {/* Add your links here */}
          <td>
            <a href="https://kstiner101-8000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/get_dealers/">Get Dealers</a>
            <a href="https://kstiner101-8000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealers/">Dealers List</a>
          </td>
        </tr>
      ))}
     </table>;
  </div>
)
}

export default Dealers
