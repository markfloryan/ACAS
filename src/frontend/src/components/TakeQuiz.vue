<template>
  <div>
    <div class="title" style="padding:10px">
      <h3>{{assignment.name}}</h3>
      <div v-if="started && !practice">
        <p>{{currentScore}}% of the way towards mastery!</p>
      </div>
    </div>
    <div class="content">
      <div v-if="!started">
        <div v-if="practice">
          This quiz is in practice mode, meaning you will be able to practice on questions very similar to the ones you might later be graded on.
          Click the start button whenever you are ready to begin practicing.
        </div>
        <div v-if="!practice">
          This quiz is in official mode, meaning you will be graded on your responses. Answer enough questions correctly in a row and the system will determine that you have
          achieved competency or mastery on this assignment.
        </div>
      </div>
      <div v-if="started && !completed">
        <MultipleChoiceQuestion
          v-if="questions[currentQuestionNumber].question_type === 0 || questions[currentQuestionNumber].question_type === 1"
          :select="questions[currentQuestionNumber].question_type === 1"
          :question="questions[currentQuestionNumber]"
          :quiz="quiz.pk"
          :key="currentQuestionNumber"
          @onSubmit="getNextQuestion()"
        />
      </div>
      <div v-if="completed">
        Congratulations! You have completed this quiz!
      </div>
    </div>
    <div class="buttons">
      <div v-if="!started">
        <center>
          <button 
            @click="startQuiz()" 
            class='btn btn-create'
            type="button"
          >Start</button>
        </center>
      </div>
      <div v-if="completed">
        <center>
          <button 
            @click="endQuiz()" 
            class='btn btn-primary'
            type="button"
          >Quit</button>
        </center>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { mapGetters, mapState, mapMutations } from 'vuex';
import { API_URL } from '@/constants';
import MultipleChoiceQuestion from '@/components/MultipleChoiceQuestion';

export default {
  components: { 
    MultipleChoiceQuestion,
  },

  data(){
    return {
      startTime: null,
      started: false,
      currentQuestionNumber: 0,
      questions: [],
      currentScore: 0,
      completed: false,
    };
  },
  mounted() {
  },
  watch: {
  },
  props: {
    courseId: {
      type: String,
      required: true,
    },
    quiz: {
      type: Object,
      required: true,
    },
    assignment: {
      type: Object,
      required: true,
    },
    practice: {
      type: Boolean,
      required: true,
    },
  },
  computed: {
    ...mapState('auth', ['profile']),
    ...mapGetters('settings', ['returnPrimaryButtonStyle']),
  },
  methods: {
    ...mapMutations('toast', ['openToast', 'setToastInfo']),
    startQuiz(){
      this.startTime = new Date(Date.now());
      this.getNextQuestion();
    },
    endQuiz(){
      this.$emit('onClose');
    },
    getNextQuestion() {
      axios.get(`${API_URL}/quiz-questions/?quiz=${this.quiz.pk}`, 
        { 
          headers: {
            'Content-Type': 'multipart/form-data',
            Authorization: `Bearer ${this.profile.id_token}`
          }
        }).then((response)=> {
        response.data.result.question_parameters = JSON.parse(response.data.result.question_parameters);
        this.questions.push(response.data.result);
        if(!this.started) {
          this.started = true;
        } else {
          this.currentQuestionNumber += 1;
        }
      }).catch(function(){
        
      });
    }
  }
};
</script>


<style scoped>
.quiz {
    display: grid;
    grid-template-areas:
        'title'
        'content'
        'buttons';
    grid-template-columns: 1fr;
    grid-template-rows: 1 1 1;
    padding: 10pt;
}
.title {
    grid-area: title;
    padding: 10pt;
}
.content {
    grid-area: content;
    padding: 10pt;
}
.buttons {
    grid-area: buttons;
    padding: 10pt;
}
</style>
