<template>
  <!-- Quiz.vue
    This component acts as a sort of if block for the different types of quizzes

    It only shows one "context" at a time, whether it be the standard view for
    taking a quiz, or quiz not found, or if you're logged in as a professor, edit/create quiz
   -->
  <div class="quiz">

    <QuizNotFound v-if="context==='quizNotFound'"
      :role="role"
      @contextChange="changeContext" />

    <QuizQuestions v-if="context==='quiz'"
      :questions="questions"
      :quizName="quizName"
      :role="role"
      :topicId="topicId"
      @contextChange="changeContext"
      @loadingChange="changeLoading" />

    <QuizResults v-if="context==='quizResults'"
      :studentQuizData="studentQuizData"
      :role="role"
      :topicId="topicId"
      @contextChange="changeContext" />

    <CreateQuiz v-if="context==='quizCreater'"
      :topicId="topicId"
      :role="role"
      @contextChange="changeContext" />

    <EditQuiz v-if="context==='quizEditor'"
      :topicId="topicId"
      :role="role"
      :initialQuizName="quizName"
      :initialQuestions="questions"
      :weight="weight"
      @contextChange="changeContext" />

    <LoadingLayer v-if="sendingAnswersInProgress"
      :message="'Saving quiz answers...'" />

  </div>
</template>

<script>
import axios from 'axios';
import { mapState } from 'vuex';
import CreateQuiz from '@/components/quiz/CreateQuiz';
import EditQuiz from '@/components/quiz/EditQuiz';
import LoadingLayer from '@/components/LoadingLayer';
import QuizNotFound from '@/components/quiz/QuizNotFound';
import QuizQuestions from '@/components/quiz/QuizQuestions';
import QuizResults from '@/components/quiz/QuizResults';
import { API_URL } from '@/constants';

export default {
  components: {
    CreateQuiz,
    EditQuiz,
    LoadingLayer,
    QuizNotFound,
    QuizQuestions,
    QuizResults,
  },
  props: {
    topicId: {
      type: Number,
    }
  },
  computed: {
    ...mapState('auth', ['profile']),
  },
  data() {
    return {
      isProfessor: false,
      quizName: '',
      questions: [],
      role: 'student',
      selectedAnswers: {},
      sendingAnswersInProgress: false,
      context: 'quiz',
      studentQuizData: {},
      weight: -1,
    };
  },
  created() {
    if (this.profile.is_professor) {
      this.role = 'professor';
    }
    this.retrieveQuiz()
      .then(this.retrieveStudentAnswers)
      .catch(() => {
        // Couldn't find quiz?
      });
  },
  methods: {
    // THis is the function that actually changes the context from showing one quiz view or another
    // ie if you're looking at the QuizQuestions.vue, and you call changeContext('quizEditor'),
    // it jumps to the EditQuiz.vue component
    changeContext(context) {
      if (context === 'quiz') {
        this.retrieveQuiz().then(() => { this.context = 'quiz'; });
      } else if (context === 'quizResults') {
        this.retrieveStudentAnswers().then(() => { this.context = 'quizResults'; });
      } else {
        this.context = context;
      }
    },
    changeLoading(isLoading) {
      this.sendingAnswersInProgress = isLoading;
    },
    // This retrieves the set of questions and answers associated with this quiz
    retrieveQuiz() {
      return new Promise((resolve, reject) => {
        axios.get(`${API_URL}/quiz/${this.topicId}`)
          .then((response) => {
            const data = response.data.result;
            this.questions = data.questions;
            this.quizName = data.name;
            this.weight = data.weight;
            
            resolve(response);
          })
          .catch((error) => {
            this.context = 'quizNotFound';
            reject(error);
          });
      });
    },
    // This attempts retrieves to retrieve a students results on the quiz if they've already taken it
    // if they have, we jump to showing the QuizResults.vue component,
    // if it fails to find them (ie student hasnt taken the quiz yet) it just shows the standard QuizQuestions.vue component
    retrieveStudentAnswers() {
      const profile = JSON.parse(localStorage.getItem('profile'));
      return new Promise((resolve, reject) => {
        let viewAs = '';
        if (this.$route.query && this.$route.query.viewAs) {
          viewAs = this.$route.query.viewAs;
        }
        axios.get(`${API_URL}/student/quiz/${this.topicId}?id_token=${profile.auth.profile.id_token}&view_as=${viewAs}`)
          .then((response) => {
            this.studentQuizData = response.data.result;
            this.sendingAnswersInProgress = false;
            this.context = 'quizResults';

            resolve();
          })
          .catch((error) => {
            reject();
          });
      });
    },
  },
};
</script>

<style>
  .quiz  .quiz-header {
    display: grid;
    grid-template-areas: 'title actions';
    grid-template-columns: 1fr 3fr;
  }
  .quiz-header > .title { grid-area: title; }
  .quiz-header > .actions { grid-area: actions; }
  .quiz {
  }
  .quiz .actions button {
    float: right;
    margin-left: 8pt;
  }
  .quiz .question {
    margin-top: 8pt;
  }
  .quiz  .question > p {
    margin: 0pt;
    margin-bottom: 3pt;
  }
  .quiz  .answers-list > .answer {
    padding-left: 8pt;
    padding-bottom: 3pt;
  }
</style>