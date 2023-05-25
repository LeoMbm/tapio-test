class Report:
    def __init__(self,name, date, _id=None):

        self._id = _id
        self.name = name
        self.date = date

    @property
    def id(self):
        return self._id


class Source:
    def __init__(self, report, description, value, emission_factor, total_emission, lifetime,
                 acquisition_year, _id=None):
        self.report = report
        self.description = description
        self.value = value
        self.emission_factor = emission_factor
        self.total_emission = total_emission
        self.lifetime = lifetime
        self.acquisition_year = acquisition_year
        self._id = _id
