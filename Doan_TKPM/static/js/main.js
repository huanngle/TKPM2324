function transcribeAudio() {
    const formData = new FormData();
    const audioInput = document.getElementById('audio-input');

    if (audioInput.files.length > 0) {
        formData.append('audio', audioInput.files[0]);

        fetch('/api/transcribe', {
            method: 'POST',
            body: formData,
        })
        .then(response => {
            console.log('Transcribe response:', response);
            if (!response.ok) {
                console.error('Transcribe response not ok:', response);
                throw new Error('Network response not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Transcribe data:', data);
            if (data.transcript) {
                document.getElementById('transcript-text').innerText = data.transcript;
                generateResponse(data.transcript);
            } else if (data.error) {
                alert(data.error);
            } else {
                alert('Transcription failed');
            }
        })
        .catch(error => {
            console.error('Transcribe error:', error);
            alert('Failed to fetch transcription.');
        });
    } else {
        alert('Please select an audio file first');
    }
}

function submitText() {
    const userInput = document.getElementById('text-input').value;
    if (userInput.trim() !== '') {
        fetchData('/api/text-input', 'POST', {'Content-Type': 'application/json'}, {input: userInput})
        .then(data => {
            console.log('Submit data:', data);
            if (data.reply) {
                document.getElementById('response-text').innerText = data.reply;
                displayFollowUpQuestions(data.follow_up_questions);
            } else if (data.error) {
                alert(data.error);
            } else {
                alert('Failed to fetch response.');
            }
        })
        .catch(error => {
            console.error('Submit error:', error);
            alert('Failed to fetch response.');
        });
    } else {
        alert('Please enter some text before submitting.');
    }
}

function generateResponse(input) {
    fetchData('/api/text-input', 'POST', {'Content-Type': 'application/json'}, {input: input})
    .then(data => {
        console.log('Generate response data:', data);
        if (data.reply) {
            document.getElementById('response-text').innerText = data.reply;
            displayFollowUpQuestions(data.follow_up_questions);
        } else if (data.error) {
            alert(data.error);
        } else {
            alert('Failed to generate response.');
        }
    })
    .catch(error => {
        console.error('response error:', error);
        alert('Failed to generate response.');
    });
}

function fetchData(url, method, headers, body) {
    return fetch(url, {
        method: method,
        headers: headers,
        body: JSON.stringify(body),
    })
    .then(response => {
        console.log('Fetch response:', response);
        if (!response.ok) {
            console.error('Fetch response not ok:', response);
            throw new Error('Network response was not ok');
        }
        return response.json();
    });
}

function displayFollowUpQuestions(questions) {
    const questionsContainer = document.getElementById('follow-up-questions');
    questionsContainer.innerHTML = '';

    if (Array.isArray(questions) && questions.length > 0) {
        questions.forEach(question => {
            const p = document.createElement('p');
            p.innerText = question;
            questionsContainer.appendChild(p);
        });
    } else {
        const p = document.createElement('p');
        p.innerText = 'No follow-up questions available.';
        questionsContainer.appendChild(p);
    }
}

