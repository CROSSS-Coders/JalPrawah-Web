<template>
  <div>
    <div>
      <base-header class="pb-6 pt-4 pt-md-8"></base-header>
      <div class="row mt--7">
        <dam-admin/>
        <user-admin/>
      </div>
    </div>
  </div>
</template>
<script>
import UserAdmin from "../components/UserAdmin";
import DamAdmin from "../components/DamAdmin";
export default {
  components: {
    UserAdmin,
    DamAdmin
  },
  data() {
    return {
    };
  },

};
</script>
<style></style>
