<template>
  <div class="question">
    <div v-if="!submitted">
      <div class="questionText">
        <h4>{{select ? "Multiple Selection" : "Multiple Choice"}}</h4>
        <h5>{{question.question_parameters.question}}</h5>
      </div>
      <sui-form class="answers">
        <div v-for="(item, index) in question.question_parameters.choices" :key="index">
          <div class="ui checkbox" style="padding-top: 6pt">
            <input type="checkbox" name="answer" v-model="selections[index]">
            <label>{{String.fromCharCode(index + 65)}}) {{item.text}}</label>
          </div>
        </div>
      </sui-form>
      <div class="submit">
        <button
            class="btn btn-create edit-btn"
            style="float: right;"
            data-toggle="tooltip"
            data-placement="bottom"
            title="Submit"
            @click="submitQuestion()"
        >Submit</button>
      </div>
    </div>
    <div v-if="submitted">
      <center>
        <h4> {{correct ? "Correct!" : "Incorrect"}} </h4>
        <h5> {{correct ? (select ? "You selected the correct answers" : "You selected the correct answer") : (select ? "You selected one or more incorrect answers" : "You selected the incorrect answer")}}</h5>
        <h5 v-if="!practice">Your score is now {{score}}%</h5>
        <button
              class="btn btn-create edit-btn"
              data-toggle="tooltip"
              data-placement="bottom"
              title="Next"
              @click="nextQuestion()"
          >Next Question</button>
      </center>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { mapGetters, mapState, mapMutations } from 'vuex';
import { API_URL } from '@/constants';
import LoadingLayer from './LoadingLayer.vue';

export default {
  components: { LoadingLayer },
  data() {
    return {
      selections: [],
      currentSelection: null,
      submitted: false,
      correct: false,
      score: 0,
    };
  },
  mounted() {
    for(let i = 0; i < this.question.question_parameters.choices.length; i += 1) {
      this.selections.push(false);
    }
  },
  watch: {
    selections: function (){
      if(!this.select) {
        if(this.currentSelection != null){
          this.selections[this.currentSelection] = false;
        }
        for(let i = 0; i < this.selections.length; i += 1) {
          if(this.selections[i]) {
            this.currentSelection = i;
            return;
          }
        }
        this.currentSelection = null;
      }
    }
  },
  computed: {
    ...mapState('auth', ['profile']),
    ...mapGetters('settings', ['returnPrimaryButtonStyle']),
  },
  props: {
    select: {
      type: Boolean,
      required: true,
    },
    quiz: {
      type: Number,
      required: true,
    },
    assignment: {
      type: Number,
      required: true,
    },
    question: {
      type: Object,
      required: true,
    },
    practice: {
      type: Boolean,
      required: true,
    }
  },
  methods: {
    ...mapMutations('toast', ['openToast', 'setToastInfo']),
    validate() {
      for(let i = 0; i < this.selections.length; i += 1) {
        if(this.selections[i]) {
          return true;
        }
      }

      this.openToast();
      this.setToastInfo({
        type: 'error',
        title: 'Error',
        message: this.select ? 'Select one or more answers' : 'Select an answer',
        duration: 10000,
      });
    },
    submitQuestion() {
      if(this.validate()){
        let choice = [];
        for(let i = 0; i < this.selections.length; i += 1) {
          if(this.selections[i]) {
            choice.push(this.question.question_parameters.choices[i].label.substring(0,1));
          }
        }

        let ret = {};
        if (!this.select) {
          ret = {
            quizPK: this.quiz,
            assignmentPK: this.assignment,
            practice_mode: this.practice,
            selection: choice[0],
          };
        } else {
          ret = {
            quizPK: this.quiz,
            assignmentPK: this.assignment,
            practice_mode: this.practice,
            all_selections: choice,
          };
        }

        axios.post(`${API_URL}/quiz-interface/${this.question.pk}`,
          ret,
          {
            headers: {
              Authorization: `Bearer ${this.profile.id_token}`
            }
          }
        ).then((response)=> {
          console.log(response.data.result);
          this.correct = response.data.result.correct;
          this.score = (response.data.result.currentQuizGrade*100).toFixed(1);
          if(this.score > 90) {
            this.$emit("onComplete")
            this.submitted = true;
          }
        }).catch((error) => {
          if (error.response.data.status == '500 - Internal Server Error') {
            this.openToast();
            this.setToastInfo({
              type: 'error',
              title: '500 - Internal Server Error',
              message: `${error}`,
              duration: 10000,
            });
          } else {
            this.openToast();
            this.setToastInfo({
              type: 'error',
              title: 'Quiz Question Submission Error',
              message: `${error}`,
              duration: 10000,
            });
          }
        });
      }
    },
    nextQuestion(){
      this.$emit('onSubmit');
    }
  },
};
</script>

<style scoped>
.question {
  display: grid;
  grid-template-areas:
      'questionText'
      'answers'
      'submit';
    grid-template-rows: auto auto auto;
}
.questionText {
  grid-area: questionText;
    padding-left: 10pt;
    padding-right: 10pt;
    padding-top: 10pt;
    padding-bottom: 10pt;
}
.answers {
  grid-area: answers;
    padding-left: 10pt;
    padding-right: 10pt;
}
.answer {
  grid-area: answer;
  display: grid;
  grid-template-areas:
      'label text';
    grid-template-columns: 1fr 20fr;
}
.label {
    grid-area: label;
    padding-left: 10pt;
    padding-right: 10pt;
    padding-top: 10pt;
    padding-bottom: 10pt;
    align-self: center;
}
.text {
    grid-area: text;
    padding-left: 10pt;
    padding-right: 10pt;
    padding-top: 10pt;
    padding-bottom: 10pt;
}
.submit {
      grid-area: submit;
    padding-left: 10pt;
    padding-right: 10pt;
    padding-top: 10pt;
    padding-bottom: 10pt;
}
</style>