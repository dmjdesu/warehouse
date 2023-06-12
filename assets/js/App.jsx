import React, { Fragment,useRef,useState, useEffect } from 'react';
import axios from 'axios';
import { ChevronDownIcon, ChevronLeftIcon, ChevronRightIcon, EllipsisHorizontalIcon } from '@heroicons/react/20/solid'
import { Menu, Transition } from '@headlessui/react'
import { baseURL } from "./export.js";
import { useWindowSize } from "./useWindowSize.js";



const App = () => {

  const container = useRef(null)
  const containerNav = useRef(null)
  const containerOffset = useRef(null)
  const [results, setResults,] = useState([]);
  const [width, height] = useWindowSize();
  const weekDays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

  // const decrementDate = () => {
  //     let previousDay = new Date(currentDate);
  //     previousDay.setDate(previousDay.getDate() - 1);
  //     setCurrentDate(previousDay);
  // }
  

  // useEffect(() => {
  //     decrementDate();
  // }, []);

  const displayDate = new Date(currentDate).getDate(); // 現在の日付を取得
  const displayDay = weekDays[new Date(currentDate).getDay()];
  
  const today = new Date();
  const formattedDate = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`;

  const [currentDate, setCurrentDate] = useState(formattedDate);

  const decreaseDateByOneDay = () => {
        let tempDate = new Date(currentDate);
        tempDate.setDate(tempDate.getDate() - 1);
        setCurrentDate(`${tempDate.getFullYear()}-${String(tempDate.getMonth() + 1).padStart(2, '0')}-${String(tempDate.getDate()).padStart(2, '0')}`);
    }

  const riseDateByOneDay = () => {
        let tempDate = new Date(currentDate);
        tempDate.setDate(tempDate.getDate() + 1);
        setCurrentDate(`${tempDate.getFullYear()}-${String(tempDate.getMonth() + 1).padStart(2, '0')}-${String(tempDate.getDate()).padStart(2, '0')}`);
    }
  const toDayByOneDay = () => {
        let tempDate = new Date();
        setCurrentDate(`${tempDate.getFullYear()}-${String(tempDate.getMonth() + 1).padStart(2, '0')}-${String(tempDate.getDate()).padStart(2, '0')}`);
    }

  const nextDate = new Date(currentDate);
  nextDate.setDate(nextDate.getDate() + 1);


  useEffect(()=>{
    axios.get(`${baseURL}parent_category?date=${currentDate}`)
      .then(res => {
        setResults(res.data.results);
        console.log(res.data.results)
      }).catch(function (error) {
        console.log(error.response);
      });
  },[currentDate])  
    

    return (
    <>
<div className="flex h-full flex-col">
      <header className="flex flex-none items-center justify-between border-b border-gray-200 px-6 py-4 sticky top-0 z-40 bg-white shadow">
  <h1 className="text-base font-semibold leading-6 text-gray-900">
    <time dateTime="2022-01">{currentDate}</time>
  </h1>
  <div className="flex items-center">
    <div className="relative flex items-center rounded-md bg-white shadow-sm md:items-stretch">
      <div
        className="pointer-events-none absolute inset-0 rounded-md ring-1 ring-inset ring-gray-300"
        aria-hidden="true"
      />
      <button
        type="button"
        onClick={decreaseDateByOneDay}
        className="flex items-center justify-center rounded-l-md py-2 pl-3 pr-4 text-gray-400 hover:text-gray-500 focus:relative md:w-9 md:px-2 md:hover:bg-gray-50"
      >
        <ChevronLeftIcon className="h-5 w-5" aria-hidden="true" />
      </button>
      <button
        type="button"
        onClick={toDayByOneDay}
        className="px-3.5 text-sm font-semibold text-gray-900 hover:bg-gray-50 focus:relative md:block"
      >
        Today
      </button>
      <span className="relative -mx-px h-5 w-px bg-gray-300 md:hidden" />
      <button
        type="button"
        onClick={riseDateByOneDay}
        className="flex items-center justify-center rounded-r-md py-2 pl-4 pr-3 text-gray-400 hover:text-gray-500 focus:relative md:w-9 md:px-2 md:hover:bg-gray-50"
      >
        <ChevronRightIcon className="h-5 w-5" aria-hidden="true" />
      </button>
    </div>
  </div>
</header>
      <div ref={container} className="isolate flex flex-auto flex-col bg-white">
        <div style={{ width: '165%' }} className="flex max-w-full flex-none flex-col md:max-w-full">
          <div
  ref={containerNav}
  className="overflow-auto sticky top-0 z-30 flex-none bg-white shadow ring-1 ring-black ring-opacity-5 sm:pr-8"
>
    <div className="grid grid-cols-3 text-sm leading-6 text-gray-500">
      <div className="flex flex-col items-center pb-3 pt-2">
        原材料
      </div>
      <button
        type="button"
        className="flex flex-col items-center pb-3 pt-2"
      >
        <span className="mt-1 flex h-8 w-8 items-center justify-center font-semibold text-gray-900">
          {new Date(currentDate).getDate()}
        </span>
      </button>
      <button
        type="button"
        className="flex flex-col items-center pb-3 pt-2"
      >
        <span className="mt-1 flex h-8 w-8 items-center justify-center font-semibold text-gray-900">
          {nextDate.getDate()}
        </span>
      </button>
    </div>
  </div>
          <div className="flex flex-auto overflow-auto">
            <ul role="list" className="divide-y flex-1 divide-gray-100">
              {results.map((result,index) => {
                return (
                  <li key={index}>
                      <div className="order-1 font-semibold">
                        <p className='text-blue-700'>{result.name}</p>
                        {result.item_set.map((item, itemIndex) => {
                          return (
                            <div key={itemIndex}>
                              <p className="text-green-500">{item.name}</p>
                              {item.material_set.map((material, materialIndex) => {
                                return <div key={materialIndex} className="h-24 text-black">
                                        <p className="text-black whitespace-nowrap">{material.name}</p>
                                      </div>
                              })}
                            </div>
                          )
                        })}
                      </div>
                  </li>
                );
              })}
              </ul>
              {/* Events */}
              <ul role="list" className="divide-y flex-1 divide-gray-100">
                {results.map((result,index) => {
                return (
                  <li key={index}>
                      <div className="order-1 font-semibold">
                        <p className='text-blue-700'>{result.name}</p>
                        {result.item_set.map((item, itemIndex) => {
                          return (
                            <div key={itemIndex}>
                              <p className="text-green-500">{item.name}</p>
                              {item.material_set.map((material, materialIndex) => {
                                console.log(material.value)
                                if (material.shopping_history_yesterday[0]) {
                                  return <div key={materialIndex} className="h-24 text-black">
                                        <label>個数:</label>
                                        <input 
                                            onChange={()=>console.log(material?.shopping_history_yesterday?.[0]?.num)} 
                                            type="text" 
                                            value={material?.shopping_history_yesterday?.[0]?.num || ''}
                                        /><br/>
                                        <label>価格:{material.shopping_history_yesterday[0].value}$
                                        </label>
                                      </div>
                                }else{
                                  return <div  key={materialIndex} className="h-24 text-black">
                                         <label>個数:</label>
                                        <input  type="text" value={0}/>
                                        <br/>
                                        <label>価格:0$</label>                                        
                                      </div>
                                }
                                
                              })}
                            </div>
                          )
                        })}
                      </div>
                  </li>
                );
              })}
              </ul>
              <ul role="list" className="divide-y flex-1 divide-gray-100">
                {results.map((result,index) => {
                return (
                  <li key={index}>
                      <div className="order-1 font-semibold">
                        <p className='text-blue-700'>{result.name}</p>
                        {result.item_set.map((item, itemIndex) => {
                          return (
                            <div key={itemIndex}>
                              <p className="text-green-500">{item.name}</p>
                              {item.material_set.map((material, materialIndex) => {
                                console.log(material)
                                if (material.shopping_history_today[0]) {
                                  return <div  key={materialIndex} className="h-24 text-black">
                                        <label>個数:</label>
                                        <input  type="text" value={material.shopping_history_today[0].num}/>
                                        <br/>
                                        <label>価格:{material.shopping_history_today[0].value}$
                                        </label>
                                      </div>
                                }else{
                                  return <div  key={materialIndex} className="h-24 text-black">
                                         <label>個数:</label>
                                        <input  type="text" value={0}/>
                                        <br/>
                                        <label>価格:0$</label>                                        
                                      </div>
                                }
                                
                              })}
                            </div>
                          )
                        })}
                      </div>
                  </li>
                );
              })}
              </ul>
              </div>
            </div>
      </div>
    </div>    </>
    );
  }
export default App;