<template>
    <div class="questionCreator">
        <div class="title" style="padding:10px">
          <h3>Add a Question</h3>
        </div>
        <div class="selector">
          <sui-form-field>
            <sui-dropdown
                placeholder="Select type of question"
                :options="questionTypes"
                selection
                search
                v-model="questionPK"
            />
          </sui-form-field>
        </div>
        <div class="content">
          <MultipleChoiceCreate 
            v-if="questionPK===0 || questionPK===1" 
            :select="questionPK===1" 
            :quiz="quiz" 
            @onClose="refreshWriter()" />
          <FreeResponseCreate 
            v-if="questionPK===2" 
            :quiz="quiz" 
            @onClose="refreshWriter()" />
          <CodingCreate 
            v-if="questionPK===3" 
            :quiz="quiz" 
            @onClose="refreshWriter()" />
          <CodeExecutionCreate 
            v-if="questionPK===4" 
            :quiz="quiz" 
            @onClose="refreshWriter()" />
        </div>
    </div>
</template>

<script>
import { mapGetters, mapState, mapMutations } from 'vuex';
import MultipleChoiceCreate from '@/components/MultipleChoiceCreate';
import FreeResponseCreate from '@/components/FreeResponseCreate';
import CodingCreate from '@/components/CodingCreate';
import CodeExecutionCreate from '@/components/CodeExecutionCreate';

export default {
  components: { MultipleChoiceCreate, FreeResponseCreate, CodingCreate, CodeExecutionCreate },
  /*
  Defines the data used by the component
  */
  data(){
    return {
      questionTypes: [],
      questionPK: null,
    };
  },
  mounted() {
    this.questionTypes = [{text: 'Multiple Choice', value: 0}, {text: 'Multiple Select', value: 1}, {text: 'Free Response', value: 2}, {text: 'Implementation', value: 3}, {text: 'Execution', value: 4}];
    if(this.question) {
      this.questionPK = this.question.question_type;
    }
  },
  watch: {
  },
  props: {
    quiz: {
      type: Number,
      required: true,
    },
    fromEdit: {
      type: Boolean,
      required: false,
    }
  },
  computed: {
    ...mapState('auth', ['profile']),
    ...mapGetters('settings', ['returnPrimaryButtonStyle']),
  },
  methods: {
    ...mapMutations('toast', ['openToast', 'setToastInfo']),
    refreshWriter() {
      if(this.fromEdit) {
        this.$emit('onClose');
      } else {
        this.questionPK = null;
      }
    },
  } 
};
</script>

<style scoped>
.questionCreator {
    display: grid;
    grid-template-areas:
        'title'
        'selector'
        'content';
    grid-template-columns: 1fr;
    grid-template-rows: 1fr 1fr 15fr
}
.title {
    grid-area: title;
    padding-left: 10pt;
    padding-right: 10pt;
}
.selector {
    grid-area: selector;
    padding-left: 10pt;
    padding-right: 10pt;
}
.content {
    grid-area: content;
    padding-left: 10pt;
    padding-right: 10pt;
}
</style>