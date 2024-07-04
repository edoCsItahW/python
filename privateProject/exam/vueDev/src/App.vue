<script>
const apiUrl = location.href + "api";


async function request(url, data, method = "POST", contentType = "application/json") {
    /*
    发送请求

    @param {string} url - 目标路径
    @param {object} data 请求内容或信号
    @return {object} 返回的json数据,包括code,msg,body
    */
    const response = await fetch(url, {
        method: method,
        headers: {"Content-Type": contentType},
        body: JSON.stringify(data)
    })

    if (!response.ok) {
        console.warn(`请求: ${location.href} => ${response.url}\n状态: ${response.statusText}(${response.status})`)
    }

    return await response.json()
}


export default {
    data() {
        return {
            response: {
                "types": null,
                "quesPool": null
            },
            quesId: 0,
            quesTitleId: 0,
            reqType: null
        }
    },
    methods: {
        reqQuesObj(quesType, varable) {

            request("/api", quesType)
                    .then(res => {
                        this.response[varable] = res.data;
                        return this.response[varable];
                    })
                    .catch(err => {
                        console.error("Error fetching data", err);
                    })
        },
        getCahceQuesObj(quesType, varable, newReq) {
            if (!this.response[varable] || newReq) {
                this.reqQuesObj(quesType, varable);
            }

            return this.response[varable];
        },
        checked(event, quesType) {
            const element = event.target

            if (element.classList.contains("checked")) {
                element.classList.remove("checked");
            }
            else {
                if (quesType === "choice" || quesType === "judge") {

                    let checkeds = document.getElementsByClassName("checked")

                    if (checkeds.length) {
                        if (checkeds[0] !== element) {
                            checkeds[0].classList.remove("checked");
                            element.classList.add("checked");
                        }
                    }
                    else {
                        element.classList.add("checked");
                    }
                }
                else if (quesType === "choiceMulti") {
                    element.classList.add("checked");
                }
            }
        },
        checkAnswer(quesObj, quesType) {

            const checkeds = Array.from(document.getElementsByClassName("checked"));

            let key = Array.from(checkeds).map(item => item.textContent[0]);

            if (quesType === "choice") {
                key = key[0];
            }

            request(apiUrl, {key: key, obj: quesObj, type: quesType})
                    .then(res => {
                        const resObj = res.data;

                        for (let elem of checkeds) elem.classList.remove("checked");

                        for (let elem of checkeds) {
                            elem.classList.remove('checked');

                            if (resObj.answer.some(item => elem.classList.contains(item))) {
                                elem.classList.add('right');
                            }
                            else {
                                elem.classList.add('incorrect');
                            }

                        }

                        for (let key of resObj.answer) {
                            document.getElementsByClassName(key)[0].classList.add('right');
                        }

                    })
        },
        nextQues() {
            for (let elem of document.getElementsByClassName("ques-option")) {
                elem.classList.remove("right");
                elem.classList.remove("incorrect");
            }

            this.quesId++;
            if (this.quesId >= this.response.quesPool.length) {
                this.quesTitleId++;

                this.getCahceQuesObj(Object.entries(this.response.types)[this.quesTitleId][0], "quesPool", true);

                this.quesId = 0;
            }
        }
    }
}
</script>

<template>
    <div class="top-container">

        <div class="ques-container">

            <h1 class="ques-title bright">{{ Object.entries(getCahceQuesObj('types', "types"))[quesTitleId][1] }}</h1>

            <div class="answering-area">

                <p class="ques-text bright">{{ `${getCahceQuesObj(Object.entries(response.types)[quesTitleId][0], "quesPool")[quesId].id}. ${response.quesPool[quesId].question}` }}</p>

                <p class="ques-option bright" :class="key" v-for="(value, key) in response.quesPool[quesId].option" @click="checked($event, Object.entries(response.types)[quesTitleId][0])">{{ `${key}. ${value}` }}</p>

                <input type="button" value="确认答案" @click="checkAnswer(response.quesPool[quesId], Object.entries(response.types)[quesTitleId][0])">

                <input type="button" value="下一题" @click="nextQues()">

            </div>

        </div>

    </div>
</template>

<style>
body {
    background-color: #202020;
}

.ques-title {
    background-image: linear-gradient(to right, #595959, #202020);
    border-radius: 5px;
    padding: 10px;
}

.answering-area {
    background-color: #3c3c3c;
    padding: 5px 10px;
    border-radius: 5px;
}

.ques-text {
    font-size: 25px;
    margin: 5px 0 0 10px;
}

.ques-option {
    background-color: #494949;
    padding: 5px;
    margin-left: 30px;
    border-radius: 5px;
}

.checked {
    background-color: #52a3ff;
}

.right {
    background-color: #afff52;
}

.incorrect {
    background-color: #ff5252;
}

.bright {
    color: white;
}

</style>
