let uuid = 1;

export default {
  mounted: function () {
    this.__uuid = 'uuid-'+uuid.toString();
    uuid += 1;
  }
}