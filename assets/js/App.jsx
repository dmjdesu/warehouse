import React, { Fragment,useRef,useState, useEffect } from 'react';
import axios from 'axios';
import { ChevronLeftIcon, ChevronRightIcon, ArrowPathIcon } from '@heroicons/react/20/solid'
import { Menu, Transition } from '@headlessui/react'
import { baseURL } from "./export.js";
import { useWindowSize } from "./useWindowSize.js";
import Select from 'react-select';
import { useCookies } from 'react-cookie';


const App = () => {

  const container = useRef(null)
  const containerNav = useRef(null)
  const containerOffset = useRef(null)
  const [results, setResults,] = useState([]);
  const [handleSubmit, setHandleSubmit,] = useState(false);
  const [category, setCategory,] = useState({ value: 'all', label: '全て' });
  const [position, setPosition,] = useState({ value: 'all', label: '全て' });
  const [targetName, setTargetName,] = useState({ value: 'all', label: '全て' });
  const [inputYesterdayValues, setInputYesterdayDayValues] = useState({});
  const [inputTodayValues, setInputTodayValues] = useState({});
  const [cookies, setCookie, removeCookie] = useCookies(['csrftoken']);
  const PositionHash ={
    'kitchen':1,
    'Sushi':2,
    'dishup':3,
  }
  

  const potion_options = [
    { value: 'all', label: '全て' },
    { value: 'kitchen', label: 'Kitchen' },
    { value: 'Sushi', label: 'Sushi' },
    { value: 'dishup', label: 'Dish Up' },
  ];

  const options = [
    { value: 'all', label: '全て' },
    { value: 'penticton', label: 'ペンティクトン店' },
    { value: 'west', label: 'ウエスト' },
    { value: 'koya', label: 'KOYA' },
    { value: 'warehouse', label: '倉庫' },
    { value: 'others', label: 'OTHERS' },
    { value: 'central', label: 'セントラルキッチン' },
  ];

  const category_options = [
    { value: 'all', label: '全て' },
    { value: 'Other', label: 'Other' },
    { value: 'Container', label: 'Container' },
    { value: 'Drinks', label: 'Drinks' },
    { value: 'Dry', label: 'Dry' },
    { value: 'Frozen', label: 'Frozen' },
    { value: 'Kitchen', label: 'Kitchen' },
    { value: 'Sushi', label: 'Sushi' },
  ];

  // 入力フィールドの値が変わった時に呼び出す関数
const handleInputYesterdayChange = (e, materialId) => {
  setInputYesterdayDayValues({
    ...inputYesterdayValues,
    [materialId]: e.target.value
  });
}

// 入力フィールドからフォーカスが外れた時に呼び出す関数
const handleYesterdayBlur = (e, materialId,total_num) => {
  submitYesterdayDate(e, materialId, total_num);
  setInputYesterdayDayValues({
    ...inputYesterdayValues,
    [materialId]: undefined // リセット
  });
}  

  // 入力フィールドの値が変わった時に呼び出す関数
const handleInputTodayChange = (e, materialId) => {
  setInputTodayValues({
    ...inputTodayValues,
    [materialId]: e.target.value
  });
}

// 入力フィールドからフォーカスが外れた時に呼び出す関数
const handleTodayBlur = (e, materialId,num) => {
  console.log("handleTodayBlur")
  console.log(e.target.value)
  submitToday(e, materialId, num);
  setInputTodayValues({
    ...inputTodayValues,
    [materialId]: undefined // リセット
  });
}  
  const today = new Date();
  const formattedDate = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`;
  console.log("formattedDate")
  console.log(formattedDate)

  const [currentDate, setCurrentDate] = useState(formattedDate);
  // const [displayDate, setDisplayDate] = useState(formattedDate);
  
  let displayFormattedYesterday = `${new Date(currentDate).getFullYear()}-${String(new Date(currentDate).getMonth() + 1).padStart(2, '0')}-${String(new Date(currentDate).getDate()).padStart(2, '0')}`;

  // Create a new Date object for yesterday's date
  const yesterday = new Date(today);
  yesterday.setDate(yesterday.getDate() - 1);

  const formattedYesterday = `${yesterday.getFullYear()}-${String(yesterday.getMonth() + 1).padStart(2, '0')}-${String(yesterday.getDate()).padStart(2, '0')}`;
  const [yesterDay, setYesterDay] = useState(formattedYesterday);

  const decreaseDateByOneDay = () => {
        let tempDate = new Date(currentDate);
        console.log("tempDate")
        console.log(tempDate)
        tempDate.setDate(tempDate.getDate() - 1);
        setCurrentDate(`${tempDate.getFullYear()}-${String(tempDate.getMonth() + 1).padStart(2, '0')}-${String(tempDate.getDate()).padStart(2, '0')}`);
    }

  const riseDateByOneDay = () => {
        let tempDate = new Date(currentDate);
        console.log("tempDate")
        console.log(tempDate)
        tempDate.setDate(tempDate.getDate() + 1);
        setCurrentDate(`${tempDate.getFullYear()}-${String(tempDate.getMonth() + 1).padStart(2, '0')}-${String(tempDate.getDate()).padStart(2, '0')}`);
    }
  const toDayByOneDay = () => {
        let tempDate = new Date();
        setCurrentDate(`${tempDate.getFullYear()}-${String(tempDate.getMonth() + 1).padStart(2, '0')}-${String(tempDate.getDate()).padStart(2, '0')}`);
    }

  const  handleChange = (targetName) => {
    setTargetName(targetName)
  }

  const  handleCategoryChange = (category) => {
    setCategory(category)
  }

  const  handlePositionChange = (position) => {
    setPosition(position)
  }
  

  const submitYesterdayDate = async (e,materialId,originNum) => {
    let format_yesterDay = `${yesterDay.getFullYear()}-${String(yesterDay.getMonth() + 1).padStart(2, '0')}-${String(yesterDay.getDate()).padStart(2, '0')}`;
    submit(e,materialId,format_yesterDay,originNum)
  }

  const submitToday  = async (e,materialId,originNum) => {
    let format_displayDate = `${currentDate.getFullYear()}-${String(currentDate.getMonth() + 1).padStart(2, '0')}-${String(currentDate.getDate()).padStart(2, '0')}`;
    
    submit(e,materialId,format_displayDate,originNum)
  }

    const submit = async (e,materialId,date,originNum) => {
        e.preventDefault();

        if (Math.floor(e.target.value) - Math.floor(originNum) === 0) return

        const data = {
            target_name: targetName.value,
            num:  e.target.value - originNum,
            material_id: materialId,
            date: date,
        }

        axios.defaults.xsrfHeaderName = "X-CSRFToken";


        try {
            const res = await axios.post(`${baseURL}react_history/`, data, {
                headers:{
                  'X-CSRFToken':cookies.csrftoken,
                  'Accept': 'application/json',
                  'Content-Type': 'application/json',
              },
            });
            setHandleSubmit(!handleSubmit)
        } catch (err) {
        }
    };
    

  useEffect(()=>{
    axios.get(`${baseURL}parent_category?date=${currentDate}&target_name=${targetName?.value}&category_name=${category?.value}`)
      .then(res => {
        setResults(res.data.results);
        console.log(res.data.results[0].item_set[0].material_set[0].shopping_history_today.date)
        setYesterDay(res.data.results[0].item_set[0].material_set[0].shopping_history_yesterday.date )
      }).catch(function (error) {
        console.log(error.response);
      });
  },[category,currentDate,targetName,handleSubmit])  
    

    return (
    <>
<div className="flex h-full flex-col">
      <header className="flex flex-none items-center justify-between border-b border-gray-200 px-6 py-4 sticky top-0 z-40 bg-white shadow">
  <h1 className="text-base font-semibold leading-6 text-gray-900">
    <time dateTime="2022-01">{displayFormattedYesterday}</time>
  </h1>
  <div className="flex flex-col items-center">
    <button
        type="button"
        onClick={()=>setHandleSubmit(!handleSubmit)}
        className="flex items-center justify-center rounded-l-md py-2 pl-3 pr-4 text-gray-400 hover:text-gray-500 focus:relative md:w-9 md:px-2 md:hover:bg-gray-50"
      >
        <ArrowPathIcon className="h-5 w-5" aria-hidden="true" />
      </button>
    <Select
        defaultValue="all"
        value={targetName}
        onChange={handleChange}
        options={options}
        placeholder="店舗を選択してください。"
      />
    <Select
        defaultValue="all"
        value={position}
        onChange={handlePositionChange}
        options={potion_options}
        placeholder="ポジションを選択してください。"
      />
    <Select
        defaultValue="all"
        value={category}
        onChange={handleCategoryChange}
        options={category_options}
        placeholder="カテゴリーを選択してください。"
      />
    <div className="relative flex items-center rounded-md bg-white shadow-sm md:items-stretch">
      <div
        className="pointer-events-none absolute inset-0 rounded-md ring-1 ring-inset ring-gray-300"
        aria-hidden="true"
      />
    </div>
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
  className="overflow-auto sticky top-120 z-30 flex-none bg-white shadow ring-1 ring-black ring-opacity-5 sm:pr-8"
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
          
          {new Date(yesterDay).getDate()}
        </span>
      </button>
      <button
        type="button"
        className="flex flex-col items-center pb-3 pt-2"
      >
        <span className="mt-1 flex h-8 w-8 items-center justify-center font-semibold text-gray-900">
          {new Date(currentDate).getDate()}
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
                                if(position.value == "all" || material.role.includes(PositionHash[position.value])){
                                  return <div key={materialIndex} className="h-24 text-black">
                                      <p className="text-black whitespace-nowrap">{material.name}</p>
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
                                if(position.value == "all" || material.role.includes(PositionHash[position.value])){
                                if (material.shopping_history_yesterday.total_num) {
                                  return <div key={materialIndex} className="h-24 text-black">
                                        <label>個数:</label>
                                        <label>個数:{material?.shopping_history_yesterday?.total_num} </label>
                                        <br/>
                                        <label>価格:{material.shopping_history_yesterday.total_value}$
                                        </label>
                                      </div>
                                }else{
                                  return <div  key={materialIndex} className="h-24 text-black">
                                         <label>個数:0</label>
                                        <br/>
                                        <label>価格:0$</label>                                        
                                      </div>
                                }
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
                                if(position.value == "all" || material.role.includes(PositionHash[position.value])){
                                if (material.shopping_history_today.total_num) {
                                  return <div  key={materialIndex} className="h-24 text-black">
                                        <label>個数:</label>
                                         { (targetName.value != 'all') ? 
                                         <input
                                          onBlur={(e) => handleTodayBlur(e, material.id,material.shopping_history_today.total_num)}
                                          onChange={(e) => handleInputTodayChange(e, material.id)}
                                          type="text"
                                          value={inputTodayValues[material.id] !== undefined ? inputTodayValues[material.id] : (material ? material?.shopping_history_today.total_num : "")}
                                        /> 
                                          : <label>個数:{material.shopping_history_today.total_num} </label>}
                                        <br/>
                                        <label>価格:{material.shopping_history_today.total_value}$
                                        </label>
                                      </div>
                                }else{
                                  return <div  key={materialIndex} className="h-24 text-black">
                                         <label>個数:</label>
                                        { (targetName.value != 'all') ?  <input 
                                            onBlur={(e) => handleTodayBlur(e, material.id,0)}
                                            onChange={(e) => handleInputTodayChange(e, material.id)}
                                            type="text" 
                                            value={inputTodayValues[material.id] !== undefined ? inputTodayValues[material.id] : (material ? material?.shopping_history_today.total_num : "")}
                                          />
                                        : <label>個数:0</label>}
                                        <br/>
                                        <label>価格:0$</label>                                        
                                      </div>
                                }
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