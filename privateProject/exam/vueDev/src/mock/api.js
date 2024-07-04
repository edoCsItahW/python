const choice = [
    {
        id: 1,
        question: "第一题...",
        option:
            {
                A: "A选项...",
                B: "B选项...",
                C: "C选项...",
                D: "D选项..."
            },
        answer: "C"
    },
    {
        id: 2,
        question: "第二题...",
        option:
            {
                A: "A选项...",
                B: "B选项...",
                C: "C选项...",
                D: "D选项..."
            },
        answer: "D"
    }
]
const choiceMulti = [
    {
        id: 1,
        question: "多选第一题...",
        option: {
            A: "A选项...",
            B: "B选项...",
            C: "C选项...",
            D: "D选项...",
            E: "E选项...",
        },
        answer: ["A", "C", "D"]
    },
    {
        id: 2,
        question: "多选第二题...",
        option: {
            A: "A选项...",
            B: "B选项...",
            C: "C选项...",
            D: "D选项...",
            E: "E选项...",
        },
        answer: ["A", "B", "D", "E"]
    }
]
const judge = [
    {
        id: 1,
        question: "判断题1...",
        option: {"A": true, "B": false},
        answer: "A"
    },
    {
        id: 2,
        question: "判断题2...",
        option: {"A": true, "B": false},
        answer: "B"
    }
]


function handle(data) {
    data = data.body;

    if (data === 'types') return {choice: "单选题", choiceMulti: "多选题", judge: "判断题"}
    else if (data === 'choice') return choice
    else if (data === 'choiceMulti') return choiceMulti
    else if (data === 'judge') return judge
    else if (typeof data === "object") {
        if (data.type === 'choice') {
            return {result: data.key === data.obj.answer, answer: [data.obj.answer]}
        }
        else if (data.type === 'choiceMulti') {

            return {result: data.obj.answer.every(item => data.key.includes(item)), answer: data.obj.answer}
        }
        else if (data.type === 'judge') {
            return {result: data.key === data.obj.answer, answer: [data.obj.answer]}
        }
    }
    else return "error"

}


export default [
    {
        url: '/api',
        method: "POST",
        response: (data) => {
            return {
                code: 200,
                msg: 'ok',
                data: handle(data)
            }
        }
    }
]