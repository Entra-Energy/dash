import { createStore } from 'vuex'

export default createStore({
  state: {
    count:0,
    path: 'day',
    selected:''

  },
  mutations: {
    increment (state, n) {
      state.count = n
    },
    setPath (state,query)
    {
      state.path = query
    },
    setSelect (state, select)
    {
      state.selected = select
    }
  },
  actions: {
  },
  modules: {
  }
})
