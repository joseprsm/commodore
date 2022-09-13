from fastapi import APIRouter

from commodore.models import Plan


router = APIRouter()


@router.post("/{space}/plans")
async def create_plan(space: str, plan: Plan):
    return plan.create(space)


@router.get("/{space}/plans")
async def get_plans(
    space: str,
    name: str = None,
    min_price: float = None,
    max_price: float = None,
    recurring: bool = None,
):
    return {"plans": Plan.list(space, name, min_price, max_price, recurring)}


@router.get("/{space}/plans/{plan_id}")
async def get_plan(space: str, plan_id: int):
    return Plan.get(space, plan_id)


@router.put("/{space}/plans/{plan_id}")
async def update_plan(space: str, plan_id: int, update: dict):
    return Plan.update(space, plan_id, update)


@router.delete("/{space}/plans/{plan_id}")
async def delete_plan(space: str, plan_id: int):
    Plan.delete(space, plan_id)
    return {"msg": f"plan {plan_id} deleted"}
