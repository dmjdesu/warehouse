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


  useEffect(()=>{
    const today = new Date();
    const date = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`;

    console.log(baseURL)
    axios.get(`${baseURL}parent_category?date=${date}`)
      .then(res => {
        setResults(res.data.results);
        console.log(res.data.results)
      }).catch(function (error) {
        console.log(error.response);
      });
  },[])  
    

    return (
    <>
<div className="flex h-full flex-col">
      <header className="flex flex-none items-center justify-between border-b border-gray-200 px-6 py-4">
        <h1 className="text-base font-semibold leading-6 text-gray-900">
          <time dateTime="2022-01">January 2022</time>
        </h1>
        <div className="flex items-center">
          <div className="relative flex items-center rounded-md bg-white shadow-sm md:items-stretch">
            <div
              className="pointer-events-none absolute inset-0 rounded-md ring-1 ring-inset ring-gray-300"
              aria-hidden="true"
            />
            <button
              type="button"
              className="flex items-center justify-center rounded-l-md py-2 pl-3 pr-4 text-gray-400 hover:text-gray-500 focus:relative md:w-9 md:px-2 md:hover:bg-gray-50"
            >
              <span className="sr-only">Previous week</span>
              <ChevronLeftIcon className="h-5 w-5" aria-hidden="true" />
            </button>
            <button
              type="button"
              className="hidden px-3.5 text-sm font-semibold text-gray-900 hover:bg-gray-50 focus:relative md:block"
            >
              Today
            </button>
            <span className="relative -mx-px h-5 w-px bg-gray-300 md:hidden" />
            <button
              type="button"
              className="flex items-center justify-center rounded-r-md py-2 pl-4 pr-3 text-gray-400 hover:text-gray-500 focus:relative md:w-9 md:px-2 md:hover:bg-gray-50"
            >
              <span className="sr-only">Next week</span>
              <ChevronRightIcon className="h-5 w-5" aria-hidden="true" />
            </button>
          </div>
          <div className="hidden md:ml-4 md:flex md:items-center">
            <Menu as="div" className="relative">
              <Menu.Button
                type="button"
                className="flex items-center gap-x-1.5 rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
              >
                Week view
                <ChevronDownIcon className="-mr-1 h-5 w-5 text-gray-400" aria-hidden="true" />
              </Menu.Button>

              <Transition
                as={Fragment}
                enter="transition ease-out duration-100"
                enterFrom="transform opacity-0 scale-95"
                enterTo="transform opacity-100 scale-100"
                leave="transition ease-in duration-75"
                leaveFrom="transform opacity-100 scale-100"
                leaveTo="transform opacity-0 scale-95"
              >
                <Menu.Items className="absolute right-0 z-10 mt-3 w-36 origin-top-right overflow-hidden rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
                  <div className="py-1">
                    <Menu.Item>
                      {({ active }) => (
                        <a
                          href="#"
                          className={classNames(
                            active ? 'bg-gray-100 text-gray-900' : 'text-gray-700',
                            'block px-4 py-2 text-sm'
                          )}
                        >
                          Day view
                        </a>
                      )}
                    </Menu.Item>
                    <Menu.Item>
                      {({ active }) => (
                        <a
                          href="#"
                          className={classNames(
                            active ? 'bg-gray-100 text-gray-900' : 'text-gray-700',
                            'block px-4 py-2 text-sm'
                          )}
                        >
                          Week view
                        </a>
                      )}
                    </Menu.Item>
                    <Menu.Item>
                      {({ active }) => (
                        <a
                          href="#"
                          className={classNames(
                            active ? 'bg-gray-100 text-gray-900' : 'text-gray-700',
                            'block px-4 py-2 text-sm'
                          )}
                        >
                          Month view
                        </a>
                      )}
                    </Menu.Item>
                    <Menu.Item>
                      {({ active }) => (
                        <a
                          href="#"
                          className={classNames(
                            active ? 'bg-gray-100 text-gray-900' : 'text-gray-700',
                            'block px-4 py-2 text-sm'
                          )}
                        >
                          Year view
                        </a>
                      )}
                    </Menu.Item>
                  </div>
                </Menu.Items>
              </Transition>
            </Menu>
            <div className="ml-6 h-6 w-px bg-gray-300" />
            <button
              type="button"
              className="ml-6 rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
            >
              Add event
            </button>
          </div>
          <Menu as="div" className="relative ml-6 md:hidden">
            <Menu.Button className="-mx-2 flex items-center rounded-full border border-transparent p-2 text-gray-400 hover:text-gray-500">
              <span className="sr-only">Open menu</span>
              <EllipsisHorizontalIcon className="h-5 w-5" aria-hidden="true" />
            </Menu.Button>

            <Transition
              as={Fragment}
              enter="transition ease-out duration-100"
              enterFrom="transform opacity-0 scale-95"
              enterTo="transform opacity-100 scale-100"
              leave="transition ease-in duration-75"
              leaveFrom="transform opacity-100 scale-100"
              leaveTo="transform opacity-0 scale-95"
            >
              <Menu.Items className="absolute right-0 z-10 mt-3 w-36 origin-top-right divide-y divide-gray-100 overflow-hidden rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
                <div className="py-1">
                  <Menu.Item>
                    {({ active }) => (
                      <a
                        href="#"
                        className={classNames(
                          active ? 'bg-gray-100 text-gray-900' : 'text-gray-700',
                          'block px-4 py-2 text-sm'
                        )}
                      >
                        Create event
                      </a>
                    )}
                  </Menu.Item>
                </div>
                <div className="py-1">
                  <Menu.Item>
                    {({ active }) => (
                      <a
                        href="#"
                        className={classNames(
                          active ? 'bg-gray-100 text-gray-900' : 'text-gray-700',
                          'block px-4 py-2 text-sm'
                        )}
                      >
                        Go to today
                      </a>
                    )}
                  </Menu.Item>
                </div>
                <div className="py-1">
                  <Menu.Item>
                    {({ active }) => (
                      <a
                        href="#"
                        className={classNames(
                          active ? 'bg-gray-100 text-gray-900' : 'text-gray-700',
                          'block px-4 py-2 text-sm'
                        )}
                      >
                        Day view
                      </a>
                    )}
                  </Menu.Item>
                  <Menu.Item>
                    {({ active }) => (
                      <a
                        href="#"
                        className={classNames(
                          active ? 'bg-gray-100 text-gray-900' : 'text-gray-700',
                          'block px-4 py-2 text-sm'
                        )}
                      >
                        Week view
                      </a>
                    )}
                  </Menu.Item>
                  <Menu.Item>
                    {({ active }) => (
                      <a
                        href="#"
                        className={classNames(
                          active ? 'bg-gray-100 text-gray-900' : 'text-gray-700',
                          'block px-4 py-2 text-sm'
                        )}
                      >
                        Month view
                      </a>
                    )}
                  </Menu.Item>
                  <Menu.Item>
                    {({ active }) => (
                      <a
                        href="#"
                        className={classNames(
                          active ? 'bg-gray-100 text-gray-900' : 'text-gray-700',
                          'block px-4 py-2 text-sm'
                        )}
                      >
                        Year view
                      </a>
                    )}
                  </Menu.Item>
                </div>
              </Menu.Items>
            </Transition>
          </Menu>
        </div>
      </header>
      <div ref={container} className="isolate flex flex-auto flex-col overflow-auto bg-white">
        <div style={{ width: '165%' }} className="flex max-w-full flex-none flex-col md:max-w-full">
          <div
            ref={containerNav}
            className="sticky top-0 z-30 flex-none bg-white shadow ring-1 ring-black ring-opacity-5 sm:pr-8"
          >
            <div className="grid grid-cols-3 text-sm leading-6 text-gray-500">
              <div className="flex flex-col items-center pb-3 pt-2">
                原材料
              </div>
              <button type="button" className="flex flex-col items-center pb-3 pt-2">
                T <span className="mt-1 flex h-8 w-8 items-center justify-center font-semibold text-gray-900">9</span>
              </button>
              <button type="button" className="flex flex-col items-center pb-3 pt-2">
                M <span className="mt-1 flex h-8 w-8 items-center justify-center font-semibold text-gray-900">10</span>
              </button>
            </div>
          </div>
          <div className="flex flex-auto">
            <ul role="list" className="divide-y flex-1 divide-gray-100">
              {results.map((result,index) => {
                return (
                  <li key={index} className="h-50">
                      <div className="order-1 font-semibold">
                        <p className='text-blue-700'>{result.name}</p>
                        {result.item_set.map((item, itemIndex) => {
                          return (
                            <div key={itemIndex}>
                              <p className="text-green-500">{item.name}</p>
                              {item.material_set.map((material, materialIndex) => {
                                return <div key={materialIndex} className="h-20 text-black">
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
                  <li key={index} className="h-50">
                      <div className="order-1 font-semibold">
                        {/* <p className='text-blue-700'>{result.name}</p> */}
                        {result.item_set.map((item, itemIndex) => {
                          return (
                            <div key={itemIndex}>
                              {/* <p className="text-green-500">{item.name}</p> */}
                              {item.material_set.map((material, materialIndex) => {
                                console.log(material.value)
                                if (material.shopping_history_yesterday[0]) {
                                  return <div key={materialIndex} className="h-16 text-black">
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
                                  return <div key={materialIndex} className="h-20 text-black">
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
                  <li key={index} className="h-50">
                      <div className="order-1 font-semibold">
                        {/* <p className='text-blue-700'>{result.name}</p> */}
                        {result.item_set.map((item, itemIndex) => {
                          return (
                            <div key={itemIndex}>
                              {/* <p className="text-green-500">{item.name}</p> */}
                              {item.material_set.map((material, materialIndex) => {
                                console.log(material)
                                if (material.shopping_history_today[0]) {
                                  return <div key={materialIndex} className="h-16 text-black">
                                        <label>個数:</label>
                                        <input  type="text" value={material.shopping_history_today[0].num}/>
                                        <br/>
                                        <label>価格:{material.shopping_history_today[0].value}$
                                        </label>
                                      </div>
                                }else{
                                  return <div key={materialIndex} className="h-20 text-black">
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