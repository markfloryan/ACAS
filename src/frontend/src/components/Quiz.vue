<template>
  <div>
    <div v-if="createQuiz === false && updateQuiz === false">
      <div class="quiz">
        <div class="title" style="padding:10px">
          <h3>Create or Update a quiz!</h3>
        </div>
        <div class="content">
          <h4>Select a Topic</h4>
          <sui-form-field>
            <sui-dropdown
            placeholder="Select topic"
            :options="topics"
            selection
            search
            v-model="topicPK"
            />
          </sui-form-field>
        </div>
        <div class="buttons">
          <button
            class="btn btn-primary edit-btn"
            :style="returnPrimaryButtonStyle"
            style="float: right;"
            data-toggle="tooltip"
            data-placement="bottom"
            title="Create Quiz"
            @click="createQuiz = true"
          >Create a new Quiz</button>
        </div>
      </div>
    </div>
    <CreateQuiz
      v-if="createQuiz"
      :courseId="courseId"
      :topicId="topicPK"
    />
    <EditQuiz
      v-if="updateQuiz"
      :courseId="courseId"
      :quizId="quizId"
    />
  </div>
</template>

<script>
import axios from 'axios';
import { mapGetters, mapState, mapMutations } from 'vuex';
import { API_URL } from '@/constants';
import CreateQuiz from '@/components/CreateQuiz';
import EditQuiz from '@/components/EditQuiz';

export default {
  components: { 
    CreateQuiz,
    EditQuiz
  },
  /*
  Defines the data used by the component
  */
  data(){
    return {
      topics: [],
      topicPK: null,
      quiz: null,
      createQuiz: false,
      updateQuiz: false,
    };
  },
  mounted() {
    this.getTopics();
  },
  watch: {
    topicPK: function() {
      this.getQuizzes();
    }
  },
  props: {
    courseId: {
      type: String,
      required: true,
    }
  },
  computed: {
    ...mapState('auth', ['profile']),
    ...mapGetters('settings', ['returnPrimaryButtonStyle']),
  },
  methods: {
    ...mapMutations('toast', ['openToast', 'setToastInfo']),
    getTopics() {
      axios.get(`${API_URL}/topics/?courseId=${this.courseId}`, 
        { 
          headers: {
            'Content-Type': 'multipart/form-data',
            Authorization: `Bearer ${this.profile.id_token}`
          }
        }).then((response)=> {
        let data = response.data.result;
        for(let i=0;i<data.length;i++){
          let topic = data[i];
          this.topics.push({
            text: topic.name,
            value: topic.pk
          });
        }
      }).catch(function(){
        
      });
    },
    getQuizzes() {
      axios.get(`${API_URL}/quizzes/?topicId=${this.topicPK}`,
        { 
          headers: {
            'Content-Type': 'multipart/form-data',
            Authorization: `Bearer ${this.profile.id_token}`
          }
        }).then((response) => {
        console.log(response.data.result);
      });
    },
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
    grid-template-rows: 1fr 8fr 1fr;
}
.title {
    grid-area: title;
    padding-left: 10pt;
    padding-right: 10pt;
}
.buttons {
    grid-area: buttons;
    padding-left: 10pt;
    padding-right: 10pt;
}
.content {
    grid-area: content;
    padding-left: 10pt;
    padding-right: 10pt;
}
</style>
