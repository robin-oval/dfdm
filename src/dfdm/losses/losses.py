import autograd.numpy as np

from dfdm.goals import goals_state


# ==========================================================================
# Loss
# ==========================================================================

class Loss:
    def __init__(self, goals, alpha=1.0, *args, **kwargs):
        self.goals = goals
        self.alpha = alpha

    def __call__(self, eqstate, model):
        gstate = self.goals_state(eqstate, model)
        return self.alpha * self.loss(gstate)

    def goals_state(self, eqstate, model):
        return goals_state(self.goals, eqstate, model)

    @staticmethod
    def loss(gstate):
        raise NotImplementedError

# ==========================================================================
# Precooked loss functions
# ==========================================================================


class SquaredError(Loss):
    """
    The canonical squared error.
    Measures the distance between the current and the target value of a goal.
    """
    @staticmethod
    def loss(gstate):
        return np.sum(gstate.weight * np.square(gstate.prediction - gstate.target))


class MeanSquaredError(Loss):
    """
    The seminal mean squared error loss.

    Average out all errors because no single error is important enough.
    """
    @staticmethod
    def loss(gstate):
        return np.mean(gstate.weight * np.square(gstate.prediction - gstate.target))


class PredictionError(Loss):
    """
    You lose when you predict too much of something.
    """
    @staticmethod
    def loss(gstate):
        return np.sum(gstate.prediction)

# ==========================================================================
# Loss container
# ==========================================================================


class Loss:
    def __init__(self, *args):
        self.loss_terms = args

    def __call__(self, q, model):
        eqstate = model(q)
        error = 0.0
        for loss in self.loss_terms:
            error += loss(eqstate, model)
        return error
