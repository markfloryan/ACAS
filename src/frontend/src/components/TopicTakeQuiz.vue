<template>
  <div class="main">
    <div v-if="state == 'StartScreen'">
      <div v-if='!loaded'>
        <h3>Loading Quiz</h3>
      </div>
      <div v-else>
        <div v-if="display_dates == true">
          <p><b>Quiz open time:</b> {{next_open_date}}</p>
          <p><b>Quiz close time:</b> {{next_close_date}}</p>
        </div>
        <br>
        <div v-if="quiz_complete == true">
          <h3>This quiz has been completed</h3>
        </div>
        <div v-else-if="quiz_open == true">
          <sui-button v-on:click="startQuiz">Start Quiz</sui-button>
        </div>
        <div v-else-if="loadError == true">
          <h3>No quiz exists for this topic</h3>
        </div>
        <div v-else>
          <h3>This quiz is currently closed</h3>
        </div>
        <br>
        <div v-if="practice_mode_open == true">
          <sui-button v-on:click="startPracticeMode">Practice Mode</sui-button>
        </div>
      </div>
    </div>
    
    <div v-else-if="state == 'TakingQuiz' && this.loaded">
        <h3> {{currentQuestion.question_text}} </h3>
        <div v-if="currentQuestion.question_type == 0">
          <div v-for="choice in currentQuestion.choices" v-bind:key="choice.id">
              <input type="radio" :id="choice.id" :value="choice.id" v-model="selection">
            <label :for="choice.id">{{choice.text}}</label>
            <br>
          </div>
        </div>
        <div v-else-if="currentQuestion.question_type == 2">
            
            <div v-for="choice in currentQuestion.choices" v-bind:key="choice.id">
              <input type="checkbox" :id="choice.id" :value="choice.id" v-model="all_selections">
            <label :for="choice.id">{{choice.text}}</label>
            <br>
            </div>
            <br>
            <p>Select all that apply</p>
        </div>
        <div v-else-if="currentQuestion.question_type == 3">
          <div class="row">
            <div class="column" style="width: 49%; vertical-align: top; display: inline-block;">
              <h3>Pool</h3>
              <draggable class="list-group" :list="list1" group="options"
                tag="ul"
                v-bind="dragOptions"
                :emptyInsertThreshold="100"
                @start="drag = true"
                @end="drag = false">
                <transition-group type="transition" :name="!drag ? 'flip-list' : null">
                <div
                  class="list-group-item"
                  v-for="element in list1"
                  :key="element.text"
                >
                  {{ element['text'] }}
                </div>
                </transition-group>
              </draggable>
            </div>

            <div class="column" style="width: 49%; vertical-align: top; display: inline-block;">
              <h3>Code</h3>
              <draggable class="list-group" :list="list2" group="options"
                tag="ul"
                v-bind="dragOptions"
                :emptyInsertThreshold="100"
                @start="drag = true"
                @end="drag = false">
                <transition-group type="transition" :name="!drag ? 'flip-list' : null">
                <div
                  class="list-group-item"
                  v-for="element in list2"
                  :key="element.text"
                >
                  {{ element['text'] }}
                </div>
                </transition-group>
              </draggable>
            </div>
          </div>
        </div>
        <div v-if="blank_answer_feeback != null">
          <h3>{{blank_answer_feeback}}</h3>
        </div>
        <div v-if="practice_mode == false">
          <h5>Question {{currentQuestion.index+1}} of {{numQuizQuestions}}</h5>
        </div>
        <div v-else>
          <center><b>Practice Mode</b></center>
        </div>
        <div>
            <sui-button v-on:click="exitQuiz">Exit Quiz</sui-button>
            <sui-button id=dynamic-button v-on:click="dynamicButtonClick">{{dynamicButtonState}}</sui-button>
        </div>
        <div v-if="dynamicButtonState != 'Submit'">
            <h2> {{submissionFeedback}} </h2>
            <div v-if="practice_mode == false">
              <h4> Current grade: {{quizGrade}} </h4>
            </div>
        </div>
    </div>
    <div v-else-if="state == 'QuizComplete'">
      <h3> Quiz Complete </h3>
      <h4> Final grade: {{quizGrade}} </h4>
      <sui-button v-on:click="exitQuiz">Exit Quiz</sui-button>
    </div>
  </div>
</template>


<script>
import axios from 'axios';
import { mapGetters, mapState, mapMutations } from 'vuex';
import { API_URL } from '@/constants';
import draggable from 'vuedraggable';

export default {
  /*
  Defines the data used by the component
  */
  components: {
    draggable,
  },
  data(){
    return{
      assignmentPK: null,
      quizPK: null,
      quizPool: {},
      quiz: [],
      practice_quiz: [],
      loadError: false,
      loaded: false,
      quiz_open: false,
      quiz_complete: false,
      practice_mode_open: false,
      practice_mode: false, // Whether or not the user is in practice mode
      next_open_date: null,
      next_close_date: null,
      display_dates: false, // Determines whether or not to display open and close dates
      selection: null, // For multiple choice questions
      all_selections: [], // For select_all questions
      code_order: [], // Chosen order for parsons problems
      quizGrade: 0,
      currentQuestion: {
        question_text: '',
        choices: [],
        options: [],
        pk: -1,
        index: 0,
        question_type: null,
      },
      state: 'StartScreen', // StartScreen, TakingQuiz, or QuizComplete
      dynamicButtonState: 'Submit', //Submit, Next, or Disabled
      currently_submitting_a_question: false,
      submissionFeedback: null,
      blank_answer_feeback: null,
      list1: [
        // { name: 'for fizzbuzz in range(51):', id: 1 },
        // { name: 'print("fizzbuzz")', id: 2 },
        // { name: 'print("buzzfizz?")', id: 3 },
        // { name: 'for dfbdbfa in adfgsdrghrg(sdgfd', id: 4 }
      ],
      list2: [
        // { name: 'for fizzbuzz in range(51):', id: 1 }
      ],
      drag: false
    };
  },
  computed: {
    ...mapState('auth', ['profile']),
    numQuizQuestions: function () {
      return this.quiz.length;
    },
    dragOptions() {
      return {
        animation: 200,
        group: 'description',
        disabled: false,
        ghostClass: 'ghost'
      };
    }
  },
  props: {
    role: {
      type: String,
      default: 'professor',
    },
    data: {
      type: Object,
    },
    topicId: {
      type: Number,
    },
  },
  mounted() {
    this.getQuiz();
  },
  // computed: {
  //   ...mapState('auth', ['profile']),
  // },
  methods: {
    ...mapMutations('toast', ['openToast', 'setToastInfo']),
    getQuiz() {
      const profile = JSON.parse(localStorage.getItem('profile'));
      axios
        .get(
          `${API_URL}/quizzes/?topicId=${this.data.topic.id}`,  { headers: { Authorization: `Bearer ${profile.auth.profile.id_token}` }}
        )
        .then(response => {
          this.assignmentPK = response.data.result.assignment;
          this.quizPK = response.data.result.pk;
          this.quizPool = JSON.parse(response.data.result.pool);
          this.quiz_open = response.data.result.allow_submissions;
          this.practice_mode_open = response.data.result.practice_mode;
          this.next_open_date = new Date(response.data.result.next_open_date).toString(); // The Date object converts the UTC time to local time
          this.next_close_date = new Date(response.data.result.next_close_date).toString();
          this.loadError = false;
        })
        .catch(error => { // If the quiz does not exist, this code is run
          this.loadError = true;
          console.log(error);
        })
        .finally(() => {
          if(this.loadError == true) { // Stop if quiz does not exists or some other error
            this.display_dates = false;
            this.loaded = true;
            console.log('Load error');
            return;
          }else if(this.quiz_open == false && this.practice_mode_open == false){ // Stop if there is no need to load the questions
            this.display_dates = true;
            this.loaded = true;
            return;
          }
          console.log('Loading quiz');
          this.display_dates = true;
          this.getQuestions('regular');
          if(this.practice_mode_open){
            this.getQuestions('practice');
          }
        },
        );
    },
    //Gets random questions based on the quiz pool
    //The algorithm is O(n), with n being the number of questions.
    // Mode is either "regular" or "practice"
    // "regular" pulls the questions that students are allowed to submit for a quiz
    // "pratice" pulls the entire quiz pool
    getQuestions(mode) {
      const profile = JSON.parse(localStorage.getItem('profile'));
      this.loaded = false;
      if(mode != 'regular' && mode != 'practice'){
        console.log('Mode must be either \'regular\' or \'practice\'');
        return;
      }
      axios
        .get(
          `${API_URL}/quiz-questions/?quiz=${this.quizPK}&mode=${mode}`,  { headers: { Authorization: `Bearer ${profile.auth.profile.id_token}` }}
        )
        .then(response => {
          let quiz_questions = response.data.result.map(function(question){
            question['question_parameters'] = JSON.parse(question['question_parameters']); // JSON parse question parameters
            return question;
          });
          quiz_questions = shuffle(quiz_questions); // Shuffle
          // Clear quizzes
          if(mode == 'regular'){
            this.quiz = [];
          }else if(mode == 'practice'){
            this.practice_quiz = [];
          }
          // Grab questions from response data and place them in the quiz list
          for(let i = 0; i < quiz_questions.length; i++) {
            let question = quiz_questions[i];
            
            if(mode == 'regular'){
              this.quiz.push(question);
            }else if(mode == 'practice'){
              this.practice_quiz.push(question);
            }
          }

          if(this.quiz_open == true && quiz_questions.length == 0){ // If quiz was open yet we get no questions, then the quiz must be complete
            this.quiz_complete = true;
          }
        })
        .catch(error => {
          console.log(error);
          this.loadError = true;
        })
        .finally(() => {
          this.loaded=true;
        });
    },
    startQuiz(){
      this.practice_mode = false;
      this.loadQuestion(0); // Load the first quiz question to start
      this.dynamicButtonState = 'Submit';
      this.state = 'TakingQuiz';
    },
    startPracticeMode(){
      this.practice_mode = true;
      this.loadQuestion(0); // Load the first quiz question to start
      this.dynamicButtonState = 'Submit';
      this.state = 'TakingQuiz';
    },
    exitQuiz(){
      this.state = 'StartScreen';
      // Shufle practice questions if exiting practice mode
      if(this.practice_mode == true){
        this.practice_quiz = shuffle(this.practice_quiz);
        this.practice_mode = false;
      }else{ // Get submittable questions if exiting the real quiz
        this.getQuestions('regular');
      }
    },
    loadQuestion(index) {
      this.selection = null; // Clear selection
      this.all_selections = []; // Clear all_selections
      this.list2 = []; // Clear list2 (The parsons answer)
      this.currentQuestion['choices'] = []; //Clear choices
      this.currentQuestion['options'] = []; //options for parsons problems only
      let quiz = this.quiz;
      if(this.practice_mode == true){
        quiz = this.practice_quiz;
      }
      if(index > quiz.length-1){ // If we are trying to load a question not in the quiz
        if(this.practice_mode == false){  // If taking the real quiz, then exit. 
          this.getQuestions('regular'); // Reload and re-shuffle questions
          this.state = 'QuizComplete';
          return;
        }else{ // If practice mode, shuffle and continue with infinite questions
          this.practice_quiz = shuffle(this.practice_quiz);
          index = 0; // reset index
        }
      }
      this.currentQuestion['index'] = index;
      this.currentQuestion['question_text'] = quiz[index]['question_parameters']['question'];
      this.currentQuestion['pk'] = quiz[index]['pk'];
      this.currentQuestion['question_type'] = quiz[index]['question_type'];

      if (this.currentQuestion['question_type'] == 0 || this.currentQuestion['question_type'] == 2) { // If multiple choice or select_all
        for (let i=0; i<quiz[index]['question_parameters']['choices'].length; i++){
          let choiceText = quiz[index]['question_parameters']['choices'][i];
          this.currentQuestion['choices'][i] = {text: choiceText, id: i};
        }
      } else if (this.currentQuestion['question_type'] == 3) { // If parsons problem
        for (let i=0; i<quiz[index]['question_parameters']['choices'].length; i++){
          let choiceText = quiz[index]['question_parameters']['choices'][i];
          this.currentQuestion['options'][i] = {text: choiceText, id: i};
        }
        this.currentQuestion['options'] = shuffle(this.currentQuestion['options']);
        this.list1 = this.currentQuestion['options'];
        this.list2 = [];
      } else {
        console.log('Question type not implemented');
      }
    },
    dynamicButtonClick() {
      if(this.dynamicButtonState === 'Submit'){
        this.submitQuestion();
      }else if(this.dynamicButtonState === 'Next'){
        this.loadQuestion(this.currentQuestion['index']+1);
        this.dynamicButtonState = 'Submit';
      }else if(this.dynamicButtonState === 'Disabled'){
        this.state = 'StartScreen';
      }
    },
    submitQuestion(){
      if(this.currently_submitting_a_question == true){ // Dont allow a question to be submitted twice by checking if one is currently being submitted
        return;
      }else{
        this.currently_submitting_a_question = true;
      }
      const profile = JSON.parse(localStorage.getItem('profile'));
      if(this.selection == null && this.all_selections.length == 0 && this.list2.length == 0){ // Dont let the user submit no answer
        this.blank_answer_feeback = 'You must answer before submitting';
        return;
      }else{
        this.blank_answer_feeback = null;
      }
      let data = {
        'quizPK': this.quizPK,
        'selection': this.selection,
        'all_selections': this.all_selections,
        'code_order': this.list2,
        'assignmentPK': this.assignmentPK,
        'question_type': this.currentQuestion.question_type,
        'practice_mode': this.practice_mode,
      };
      axios
        .post(`${API_URL}/quiz-interface/${this.currentQuestion['pk']}/`, data, { headers: { Authorization: `Bearer ${profile.auth.profile.id_token}` } })
        .then(response => {
          this.quizGrade = Math.round(response.data.result.currentQuizGrade * 100);
          if (response.data.result.correct){
            this.submissionFeedback = 'Correct';
            this.dynamicButtonState = 'Next';
          }else{
            this.submissionFeedback = 'Incorrect';
            this.dynamicButtonState = 'Next';
          }
          this.currently_submitting_a_question = false; // Mark the end of the question submission
        })
        .catch(error => {
          this.submissionFeedback = error.response.data.result.info;
          this.dynamicButtonState = 'Disabled'; // Disable the next button if the quiz is no longer accepting responses
          this.quiz_open = false;
          this.currently_submitting_a_question = false; // Mark the end of the question submission
        })
        .finally(() => {
          
        });
    },
  } 
};

var shuffle = function (array) {

  var currentIndex = array.length;
  var temporaryValue, randomIndex;

  // While there remain elements to shuffle...
  while (0 !== currentIndex) {
    // Pick a remaining element...
    randomIndex = Math.floor(Math.random() * currentIndex);
    currentIndex -= 1;

    // And swap it with the current element.
    temporaryValue = array[currentIndex];
    array[currentIndex] = array[randomIndex];
    array[randomIndex] = temporaryValue;
  }

  return array;
};
</script>

<style scoped>
#dynamic-button{
  float: right;
}

.flip-list-move {
  transition: transform 0.5s;
}
.no-move {
  transition: transform 0s;
}
.ghost {
  opacity: 0.5;
  background: #c8ebfb;
}
.list-group {
  min-height: 20px;
  padding-left: 0;
}
.list-group-item {
  cursor: move;
  list-style-type: none;
  background-color: #DDDDDD;
	border: 2px solid #AAAAAA;
  border-radius: 8px;
	color: #000000;
	padding: 0.3em 1em;
	text-align: left;
	text-decoration: none;
	font-size: 1em;
	/* display: inline-block; */
	width: 100%; /* to test the test-align property */
}
.list-group-item i {
  cursor: pointer;
}

ul {
  padding: none;
}

.row {
  width: 100%;
}

.column {
  width: 50%;
}
</style>
