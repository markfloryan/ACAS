import Vue from 'vue';
import TopicStudentGrade from '@/components/TopicStudentGrade';

describe('TopicStudentGrade.vue', () => {
  // First Unit test
  it('Does topicstudentgrade data exist', () => {
    const Constructor = Vue.extend(TopicStudentGrade);
    const vm = new Constructor().$mount();
    Vue.nextTick(() =>{
      expect(vm.$el.data().exists()).to.equal(true);
      done();
    });
  });
  
  it('Instance can be run', () => {
    const Constructor = Vue.extend(TopicStudentGrade);
    const vm = new Constructor().$mount();
    Vue.nextTick(() =>{
      expect(vm.$el.exists()).to.equal(true);
      done();
    });
  });

  it('Test the role of the vue', () => {
    const Constructor = Vue.extend(TopicStudentGrade);
    const vm = new Constructor().$mount();
    Vue.nextTick(() =>{
      expect(vm.$el.props.role).to.equal('student');
      done();
    });
  });


  it('test result array to be empty', () => {
    const Constructor = Vue.extend(TopicStudentGrade);
    const vm = new Constructor().$mount();
    Vue.nextTick(() =>{
      expect(vm.$el.data().grades.exists()).to.equal(true);
      done();
    });
  });
  
  
  it('Does readingtext array exists', () => {
    const Constructor = Vue.extend(TopicStudentGrade);
    const vm = new Constructor().$mount();
    Vue.nextTick(() =>{
      expect(vm.$el.data().exists()).to.equal(true);
      done();
    });
  });
});
  
