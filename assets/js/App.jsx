import React, { Fragment, useRef, useState, useEffect } from "react";
import axios from "axios";
import {
  ChevronLeftIcon,
  ChevronRightIcon,
  ArrowPathIcon,
} from "@heroicons/react/20/solid";
import { Menu, Transition } from "@headlessui/react";
import { baseURL } from "./export.js";
import { useWindowSize } from "./useWindowSize.js";
import Select from "react-select";
import { useCookies } from "react-cookie";
import { DateTime } from "luxon";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import { FaCalendarAlt } from "react-icons/fa";
import { AiFillCheckCircle } from "react-icons/ai";
import ReactLoading from "react-loading";
import Modal from "react-modal";

const App = () => {
  let subtitle;
  const customStyles = {
    content: {
      top: "50%",
      left: "50%",
      right: "auto",
      bottom: "auto",
      marginRight: "-50%",
      transform: "translate(-50%, -50%)",
    },
  };

  function openModal() {
    setIsOpen(true);
  }

  function afterOpenModal() {
    // references are now sync'd and can be accessed.
    subtitle.style.color = "#f00";
  }

  function closeModal() {
    setIsOpen(false);
  }
  const [modalIsOpen, setIsOpen] = useState(false);
  const container = useRef(null);
  const containerNav = useRef(null);
  const [changedMaterials, setChangedMaterials] = useState({});
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState([]);
  const [handleReload, setHandleReload] = useState(false);
  const [category, setCategory] = useState({ value: "all", label: "種類全て" });
  const [position, setPosition] = useState({
    value: "all",
    label: "ポジション全て",
  });
  const [targetName, setTargetName] = useState({
    value: "all",
    label: "店舗全て",
  });
  const [inputTodayValues, setInputTodayValues] = useState({});
  const [cookies, setCookie, removeCookie] = useCookies(["csrftoken"]);
  const PositionHash = {
    kitchen: 1,
    Sushi: 2,
    dishup: 3,
  };

  const potion_options = [
    { value: "all", label: "ポジション全て" },
    { value: "kitchen", label: "Kitchen" },
    { value: "Sushi", label: "Sushi" },
    { value: "dishup", label: "Dish Up" },
  ];

  const options = [
    { value: "all", label: "店舗全て" },
    { value: "penticton", label: "ペンティクトン店" },
    { value: "west", label: "ウエスト" },
    { value: "koya", label: "KOYA" },
    { value: "warehouse", label: "倉庫" },
    { value: "others", label: "OTHERS" },
    { value: "central", label: "セントラルキッチン" },
  ];

  const category_options = [
    { value: "all", label: "種類全て" },
    { value: "Other", label: "Other" },
    { value: "Container", label: "Container" },
    { value: "Drinks", label: "Drinks" },
    { value: "Dry", label: "Dry" },
    { value: "Frozen", label: "Frozen" },
    { value: "Kitchen", label: "Kitchen" },
    { value: "Sushi", label: "Sushi" },
    { value: "amazake sause", label: "amazake sause" },
  ];

  // 入力フィールドの値が変わった時に呼び出す関数
  const handleInputTodayChange = (e, materialId) => {
    setInputTodayValues({
      ...inputTodayValues,
      [materialId]: e.target.value,
    });
  };

  // 入力フィールドからフォーカスが外れた時に呼び出す関数
  const handleTodayBlur = (e, materialId, newTotalNum) => {
    // 現在の changedMaterials のコピーを作成
    const updatedChangedMaterials = { ...changedMaterials };

    // 文字列から数値への変換
    newTotalNum = Number(newTotalNum);

    // 全ての results のコピーを作成
    const updatedResults = [...results];

    // 各結果に対して
    for (let result of updatedResults) {
      // 各 item に対して
      for (let item of result.item_set) {
        // 各 material に対して
        for (let material of item.material_set) {
          // 材料の ID が一致するかどうかをチェック
          if (material.id === materialId) {
            if (e.target.value - material.shopping_history_today.total_num == 0)
              return;
            // 一致する場合、新しい値を使って更新情報を作成
            updatedChangedMaterials[materialId] = {
              oldTotalNum: material.shopping_history_today.total_num,
              newTotalNum: e.target.value,
              name: material.name,
            };
            // 一致する場合、材料の total_num を新しい値で更新
            material.shopping_history_today.total_num = newTotalNum;
            material.shopping_history_today.total_value =
              newTotalNum * material.value;
            // state を更新
            setResults(updatedResults);
            setChangedMaterials(updatedChangedMaterials);
            // 更新が完了したら、ループを抜ける
            return;
          }
        }
      }
    }
  };

  // Get the current date in Ohio
  const currentDateInOhio = DateTime.now().setZone("America/New_York");
  const formattedDate = `${currentDateInOhio.year}-${String(
    currentDateInOhio.month
  ).padStart(2, "0")}-${String(currentDateInOhio.day).padStart(2, "0")}`;

  const [currentDate, setCurrentDate] = useState(formattedDate);

  // Get yesterday's date in Ohio
  const yesterdayInOhio = currentDateInOhio.minus({ days: 1 });
  const formattedYesterday = `${yesterdayInOhio.year}-${String(
    yesterdayInOhio.month
  ).padStart(2, "0")}-${String(yesterdayInOhio.day).padStart(2, "0")}`;

  const [yesterDay, setYesterDay] = useState(formattedYesterday);

  const handleChange = (targetName) => {
    setTargetName(targetName);
  };

  const handleCategoryChange = (category) => {
    setCategory(category);
    setHandleReload(!handleReload);
  };

  const handlePositionChange = (position) => {
    setPosition(position);
  };

  const handleChangeDate = (date) => {
    let tempDate = DateTime.fromJSDate(date, { zone: "America/New_York" });
    tempDate = tempDate.plus({ days: 1 });

    const year = tempDate.year;
    const month = String(tempDate.month).padStart(2, "0");
    const day = String(tempDate.day).padStart(2, "0");

    setCurrentDate(`${year}-${month}-${day}`);
    setChangedMaterials({});
  };

  const submit = async (materialId, date, oldTotalNum, newTotalNum) => {
    console.log("newTotalNum");
    console.log(newTotalNum - oldTotalNum);
    if (newTotalNum - oldTotalNum === 0) return;

    const data = {
      target_name: targetName.value,
      num: newTotalNum - oldTotalNum,
      material_id: materialId,
      date: date,
    };

    axios.defaults.xsrfHeaderName = "X-CSRFToken";

    try {
      const res = await axios.post(`${baseURL}react_history/`, data, {
        headers: {
          "X-CSRFToken": cookies.csrftoken,
          Accept: "application/json",
          "Content-Type": "application/json",
        },
      });
    } catch (err) {}
  };

  const handleMultipleSubmit = async () => {
    let format_displayDate = `${new Date(currentDate).getFullYear()}-${String(
      new Date(new Date(currentDate)).getMonth() + 1
    ).padStart(2, "0")}-${String(new Date(currentDate).getDate()).padStart(
      2,
      "0"
    )}`;
    const promises = Object.keys(changedMaterials).map((materialId) => {
      const material = changedMaterials[materialId];
      return submit(
        materialId,
        format_displayDate, // 日付の値を適切に設定する必要があります
        material.oldTotalNum,
        material.newTotalNum
      );
    });

    try {
      await Promise.all(promises);
      console.log("All materials have been submitted.");
    } catch (err) {
      console.error(err);
    } finally {
      setHandleReload(!handleReload);
      closeModal();
      setChangedMaterials({});
    }
  };

  useEffect(() => {
    setLoading(true);
    axios
      .get(
        `${baseURL}parent_category?date=${currentDate}&target_name=${targetName?.value}&category_name=${category?.value}`
      )
      .then((res) => {
        setResults(res.data.results);
        setYesterDay(
          res.data.results[0].item_set[0].material_set[0]
            .shopping_history_yesterday.date
        );
      })
      .catch(function (error) {
        console.log(error.response);
      })
      .finally(function () {
        setLoading(false);
      });
  }, [category, currentDate, targetName, handleReload]);

  return (
    <>
      <Modal
        isOpen={modalIsOpen}
        onAfterOpen={afterOpenModal}
        onRequestClose={closeModal}
        style={customStyles}
        contentLabel="Example Modal"
      >
        <div className="h-full overflow-y-auto">
          {Object.keys(changedMaterials).map((materialId) => {
            const material = changedMaterials[materialId];
            return (
              <div
                key={materialId}
                className="flex justify-between items-center"
              >
                <p className="flex-1">
                  {material.name}:元々の個数: {material.oldTotalNum ?? 0}{" "}
                  新しい個数:
                  {material.newTotalNum}
                </p>
              </div>
            );
          })}
        </div>
        <div className="flex justify-end mt-4">
          <button
            className="flex-1 px-4 py-2 bg-gray-300 mr-2"
            onClick={closeModal}
          >
            キャンセル
          </button>
          <button
            className="flex-1 px-4 py-2 bg-blue-600 text-white"
            onClick={handleMultipleSubmit}
          >
            送信
          </button>
        </div>
      </Modal>
      {loading && (
        <ReactLoading
          type={"balls"}
          color={"blue"}
          height={"20%"}
          width={"20%"}
        />
      )}
      <div className="flex h-full flex-col">
        <header className="flex flex-none items-center justify-between border-b border-gray-200 px-6 py-4 sticky top-0 z-40 bg-white shadow">
          <h1 className="text-base font-semibold leading-6 text-gray-900">
            <time dateTime="2022-01">{currentDate}</time>
          </h1>
          <div className="flex flex-col sm:flex-row items-center">
            <button
              type="button"
              onClick={() => setHandleReload(!handleReload)}
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
              <DatePicker
                selected={new Date(currentDate)}
                customInput={
                  <button
                    type="button"
                    className="inline-flex items-center gap-x-1.5 rounded-md bg-indigo-600 px-2.5 py-1.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                  >
                    <FaCalendarAlt />
                    Choice date
                  </button>
                }
                onChange={handleChangeDate}
              />
              <button
                type="button"
                className="inline-flex items-center gap-x-1.5 p-2.5 rounded bg-lime-500 px-2 py-1 text-xs font-semibold text-white shadow-sm hover:bg-lime-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-lime-600"
                onClick={openModal}
              >
                <AiFillCheckCircle /> 確定する
              </button>
            </div>
          </div>
        </header>
        <div
          ref={container}
          className="isolate flex flex-auto flex-col bg-white"
        >
          <div
            style={{ width: "165%" }}
            className="flex max-w-full flex-none flex-col md:max-w-full"
          >
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
                {results.map((result, index) => {
                  return (
                    <li key={index}>
                      <div className="order-1 font-semibold">
                        <p className="text-blue-700">{result.name}</p>
                        {result.item_set.map((item, itemIndex) => {
                          return (
                            <div key={itemIndex}>
                              <p className="text-green-500">{item.name}</p>
                              {item.material_set.map((material) => {
                                if (
                                  position.value == "all" ||
                                  material.role.includes(
                                    PositionHash[position.value]
                                  )
                                ) {
                                  return (
                                    <div
                                      key={material.id}
                                      className="h-24 text-black"
                                    >
                                      <p className="text-black whitespace-nowrap">
                                        {material.name}
                                      </p>
                                    </div>
                                  );
                                }
                              })}
                            </div>
                          );
                        })}
                      </div>
                    </li>
                  );
                })}
              </ul>
              {/* Events */}
              <ul role="list" className="divide-y flex-1 divide-gray-100">
                {results.map((result, index) => {
                  return (
                    <li key={index}>
                      <div className="order-1 font-semibold">
                        <p className="text-blue-700">{result.name}</p>
                        {result.item_set.map((item, itemIndex) => {
                          return (
                            <div key={itemIndex}>
                              <p className="text-green-500">{item.name}</p>
                              {item.material_set.map((material) => {
                                if (
                                  position.value == "all" ||
                                  material.role.includes(
                                    PositionHash[position.value]
                                  )
                                ) {
                                  if (
                                    material.shopping_history_yesterday
                                      .total_num
                                  ) {
                                    return (
                                      <div
                                        key={material.id}
                                        className="h-24 text-black"
                                      >
                                        <label>
                                          個数:
                                          {
                                            material?.shopping_history_yesterday
                                              ?.total_num
                                          }{" "}
                                        </label>
                                        <br />
                                        <label>
                                          価格:
                                          {
                                            material.shopping_history_yesterday
                                              .total_value
                                          }
                                          $
                                        </label>
                                      </div>
                                    );
                                  } else {
                                    return (
                                      <div
                                        key={material.id}
                                        className="h-24 text-black"
                                      >
                                        <label>個数:0</label>
                                        <br />
                                        <label>価格:0$</label>
                                      </div>
                                    );
                                  }
                                }
                              })}
                            </div>
                          );
                        })}
                      </div>
                    </li>
                  );
                })}
              </ul>
              <ul role="list" className="divide-y flex-1 divide-gray-100">
                {results.map((result, index) => {
                  return (
                    <li key={index}>
                      <div className="order-1 font-semibold">
                        <p className="text-blue-700">{result.name}</p>
                        {result.item_set.map((item, itemIndex) => {
                          return (
                            <div key={itemIndex}>
                              <p className="text-green-500">{item.name}</p>
                              {item.material_set.map((material) => {
                                if (
                                  position.value == "all" ||
                                  material.role.includes(
                                    PositionHash[position.value]
                                  )
                                ) {
                                  if (
                                    material.shopping_history_today.total_num
                                  ) {
                                    return (
                                      <div
                                        key={material.id}
                                        className="h-24 text-black"
                                      >
                                        <label>個数:</label>
                                        {targetName.value != "all" ? (
                                          <input
                                            onBlur={(e) =>
                                              handleTodayBlur(
                                                e,
                                                material.id,
                                                material.shopping_history_today
                                                  .total_num
                                              )
                                            }
                                            onChange={(e) =>
                                              handleInputTodayChange(
                                                e,
                                                material.id
                                              )
                                            }
                                            type="text"
                                            value={
                                              inputTodayValues[material.id] !==
                                              undefined
                                                ? inputTodayValues[material.id]
                                                : material
                                                    .shopping_history_today
                                                    .total_num
                                            }
                                          />
                                        ) : (
                                          <label>
                                            個数:
                                            {
                                              material.shopping_history_today
                                                .total_num
                                            }{" "}
                                          </label>
                                        )}
                                        <br />
                                        <label>
                                          価格:
                                          {
                                            material.shopping_history_today
                                              .total_value
                                          }
                                          $
                                        </label>
                                      </div>
                                    );
                                  } else {
                                    return (
                                      <div
                                        key={material.id}
                                        className="h-24 text-black"
                                      >
                                        <label>個数:</label>
                                        {targetName.value != "all" ? (
                                          <input
                                            onBlur={(e) =>
                                              handleTodayBlur(e, material.id, 0)
                                            }
                                            onChange={(e) =>
                                              handleInputTodayChange(
                                                e,
                                                material.id
                                              )
                                            }
                                            type="text"
                                            value={
                                              inputTodayValues[material.id] !==
                                              undefined
                                                ? inputTodayValues[material.id]
                                                : material
                                                    ?.shopping_history_today
                                                    .total_num
                                            }
                                          />
                                        ) : (
                                          <label>個数:0</label>
                                        )}
                                        <br />
                                        <label>価格:0$</label>
                                      </div>
                                    );
                                  }
                                }
                              })}
                            </div>
                          );
                        })}
                      </div>
                    </li>
                  );
                })}
              </ul>
            </div>
          </div>
        </div>
      </div>{" "}
    </>
  );
};
export default App;
