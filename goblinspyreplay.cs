//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
using System;
using System.Collections.Generic;
using BB2StatsLib.BB2Replay;


namespace BB2StatsLib.Views.Replay
{
	[Serializable]
	public class ReplayView
	{
		public List<ReplayItem> Items{ get; set; }
        public List<ReplayBlockAction> Blocks { get; set; }
        public List<ReplayMoveAction> Moves { get; set; }
        public List<ReplayRollAction> Rolls { get; set; }
        public List<ReplayInjuryAction> Injuries { get; set; }
        public List<ReplayInjuryAction> Casualties { get; set; }
        public List<ReplayActionKickoff> Kickoffs { get; set; }
        public List<ReplayEndTurnAction> EndTurns { get; set; }
        public List<ReplayBallAction> Balls { get; set; }
        
        public ReplayView()
		{
            Items = new List<ReplayItem>();
            Blocks = new List<ReplayBlockAction>();
            Moves = new List<ReplayMoveAction>();
            Rolls = new List<ReplayRollAction>();
            Injuries = new List<ReplayInjuryAction>();
            Casualties = new List<ReplayInjuryAction>();
            Kickoffs = new List<ReplayActionKickoff>();
            EndTurns = new List<ReplayEndTurnAction>();
            Balls = new List<ReplayBallAction>();
        }

		public static ReplayView CreateFromReplay(BB2Replay.Replay replay)
		{
			ReplayView newReplay = new ReplayView ();
			newReplay.Parse (replay);
			return newReplay;
		}

		public void Parse(BB2Replay.Replay replay)
		{
            int lastItemCausingArmorTest = 0;
            int iTurn = 0;

            // Grab a player dictionary
            Dictionary<int, int> localIdToGlobalId = new Dictionary<int, int>();
            bool gotContent = false;
            foreach (ReplayStep step in replay.ReplayStep)
            {
                if(step.RulesEventGameFinished != null)
				{
					if(step.RulesEventGameFinished.MatchResult.CoachResults != null)
					{
                        int i=0;
						foreach( CoachResult res in step.RulesEventGameFinished.MatchResult.CoachResults)
						{
                                	
                            foreach (PlayerResult ps in res.TeamResult.PlayerResults)
                            {
                                if (ps.Statistics.IdPlayerListing != 0)
                                    gotContent = true;
                                localIdToGlobalId[ps.PlayerData.Id] = ps.Statistics.IdPlayerListing;
                                if (ps.Statistics.IdPlayerListing < 100) // loner
                                {
                                    int lonerId = ps.Statistics.IdPlayerListing;
                                    if (ps.PlayerData.Name == null)
                                        ps.PlayerData.Name = "unknown";
                                    int pid = lonerId+Math.Abs(ps.PlayerData.Name.GetHashCode()) + res.TeamResult.IdTeam;
                                    localIdToGlobalId[ps.PlayerData.Id] = pid;
                                }
                            }

                                
                            i++;
                        }
                    }
                }
                if (gotContent)
                    break;
            }
            // ANd then go through the replays
            Dictionary<string, int> positionMap = new Dictionary<string, int>();
            int lastPlayer = 0;
            int playerFirstIndex = -1;
            bool lastPlayerBlocked = false;
            bool lastPlayerMoved = false;
            ReplayActionPosition ballPos = new ReplayActionPosition();
            bool nextRed = false;

            foreach (BB2Replay.ReplayStep step in replay.ReplayStep)
			{
                if(step.BoardState != null && step.BoardState.ListTeams != null)
                {
                    foreach(var ts in step.BoardState.ListTeams)
                    {
                        if(ts.ListPitchPlayers != null)
                        {
                            foreach(var ps in ts.ListPitchPlayers)
                            {
                                positionMap[ps.Cell.ToString()] = ps.Id;
                            }
                        }
                    }
                }
               

                if (step.RulesEventKickOffTable != null)
                {
                    ReplayActionKickoff rekot = new ReplayActionKickoff(
                     step.RulesEventKickOffTable.Event
                     );

                    Kickoffs.Add(rekot);
                    Items.Add(new ReplayItem(ReplayItemType.KickoffEvent, Kickoffs.Count - 1, -1));
              
                }

                if (step.RulesEventEndTurn != null)
                {
                    if (step.RulesEventEndTurn.TouchdownScorer > 0 )//!= -1)
                    {
                        Items.Add(new ReplayItem(ReplayItemType.Touchdown, Moves.Count - 1, 
                            localIdToGlobalId[
                            step.RulesEventEndTurn.TouchdownScorer]));
                    }
                    int nextTeamIndex = step.RulesEventEndTurn.PlayingTeam;
                    ReplayEndTurnAction eta = new ReplayEndTurnAction(
                        step.BoardState.ListTeams[nextTeamIndex].GameTurn,
                        nextTeamIndex,
                        step.BoardState.ListTeams[nextTeamIndex].RerollNumber,
                        step.BoardState.Ball
                        );

                    iTurn++;
                    EndTurns.Add(eta);
                    Items.Add(new ReplayItem(ReplayItemType.EndTurn, EndTurns.Count - 1, -1));

                    foreach (TeamState ts in step.BoardState.ListTeams)
                    {
                        foreach (PlayerState ps in ts.ListPitchPlayers)
                        {
                           positionMap[ps.Cell.ToString()] = ps.Id;
                           eta.Players.Add(new ReplayPlayer(localIdToGlobalId[ps.Id], ps.Cell, (ps.CanAct == 0 )? 2 : ps.MovePoint < ps.Data.Ma ? 1 : 0));
                        }
                    }
                }

				if(step.RulesEventBoardAction != null)
				{
                    foreach (RulesEventBoardAction ba in step.RulesEventBoardAction)
                    {
                        

                        if(ba.Order!=null && ba.Order.CellFrom != null )
                            positionMap[ba.Order.CellFrom.ToString()] = ba.PlayerId;
                        if(ba.Results != null)
                        {
                            foreach (BoardActionResult bar in ba.Results.BoardActionResult)
                            {
                                ReplayItemType type = (ReplayItemType)bar.RollType;


                                if(type == ReplayItemType.Move || type == ReplayItemType.Dodge || type == ReplayItemType.Leap ||
                                    type == ReplayItemType.Block)
                                {
                                    if (ba.PlayerId >= 0 && localIdToGlobalId.ContainsKey(ba.PlayerId))
                                    {
                                        int curPlayerId = localIdToGlobalId[ba.PlayerId];
                                        if (lastPlayer != curPlayerId)
                                        {
                                            if (lastPlayerMoved && lastPlayerBlocked && playerFirstIndex >= 0)
                                            {
                                                ReplayItem blitzAction = new ReplayItem(ReplayItemType.Blitz, -1, lastPlayer);
                                                Items.Insert(playerFirstIndex, blitzAction);
                                                lastItemCausingArmorTest++; // gets pushed forward due to blitz inserted
                                            }
                                            lastPlayerBlocked = false;
                                            lastPlayerMoved = false;
                                            playerFirstIndex = Items.Count;
                                            lastPlayer = curPlayerId;
                                        }
                                    }
                                }

                                switch(type)
                                {
                                    case ReplayItemType.Dodge:
                                    case ReplayItemType.Leap:
                                    case ReplayItemType.Move:
                                    case ReplayItemType.Push:
                                    case ReplayItemType.FollowUp:
                                        if (bar.IsOrderCompleted == 0)
                                            break;

                                        if (ba.Order.CellFrom.x != ba.Order.CellTo.Cell.x ||
                                            ba.Order.CellFrom.y != ba.Order.CellTo.Cell.y)
                                        {
                                            if(type != ReplayItemType.Push && type != ReplayItemType.FollowUp)
                                                lastPlayerMoved = true;
                                            positionMap[ba.Order.CellTo.Cell.ToString()] = ba.PlayerId;
                                        }
                                         break; 
                                }
                                switch (type)
                                {
                                    case ReplayItemType.Armor:
                                        if (bar.CoachChoices.ListDices != null)
                                        {
                                            ReplayRollAction rda = new ReplayRollAction(bar.Requirement - GetModifierSum(bar.ListModifiers), ReplayActionBase.ParseDices(bar.CoachChoices.ListDices), ba.Order.CellTo.Cell, bar.IsOrderCompleted == 0);
                                            Rolls.Add(rda);


                                            Items.Add(new ReplayItem(type, Rolls.Count - 1, localIdToGlobalId[ba.PlayerId]));
                                            try
                                            {
                                                ReplayItem it = Items[lastItemCausingArmorTest];
                                                if (it.AID == (int)ReplayItemType.Block)
                                                    Blocks[it.I].TID = localIdToGlobalId[ba.PlayerId];
                                            }
                                            catch { }
                                        }
                                        break;
                                    case ReplayItemType.Dodge:
                                    case ReplayItemType.Leap:
                                    case ReplayItemType.Pass:
                                    case ReplayItemType.Catch:
                                    case ReplayItemType.GFI:
                                    case ReplayItemType.Pickup:
                                    case ReplayItemType.Foul:
                                  

                                        if (localIdToGlobalId.ContainsKey(ba.PlayerId) && bar.CoachChoices.ListDices != null)
                                        {
                                            ReplayRollAction rda =
                                                new ReplayRollAction(bar.Requirement - GetModifierSum(bar.ListModifiers), ReplayActionBase.ParseDices(bar.CoachChoices.ListDices),
                                                ba.Order.CellTo.Cell, bar.IsOrderCompleted == 0
                                                );
                                            Rolls.Add(rda);
                                            Items.Add(new ReplayItem(type, Rolls.Count - 1, localIdToGlobalId[ba.PlayerId]));
                                        }
                                        

                                        break;
                                    case ReplayItemType.Bonehead:
                                    case ReplayItemType.WildAnimal:

                                        if (localIdToGlobalId.ContainsKey(ba.PlayerId) && bar.CoachChoices.ListDices != null)
                                        {
                                            ReplayRollAction rda =
                                                new ReplayRollAction(bar.Requirement - GetModifierSum(bar.ListModifiers), ReplayActionBase.ParseDices(bar.CoachChoices.ListDices),
                                                ba.Order.CellTo.Cell, bar.IsOrderCompleted == 0
                                                );
                                            Rolls.Add(rda);
                                            Items.Add(new ReplayItem(type, Rolls.Count - 1, localIdToGlobalId[ba.PlayerId]));
                                        }
                                        break;
                                    case ReplayItemType.Block:
                                        lastPlayerBlocked = true;
                                        if (bar.IsOrderCompleted==0) // Beginning of block, the rolled dices
                                        {
                                            int targetPlayer = -1;
                                            positionMap.TryGetValue(ba.Order.CellTo.Cell.ToString(), out targetPlayer);

                                            

                                            ReplayBlockAction rba = new ReplayBlockAction(bar.CoachChoices.ListDices, targetPlayer > 0 ? localIdToGlobalId[targetPlayer] : -1);
                                            if (bar.RequestType == 1)
                                            {
                                                nextRed = true;

                                            }
                                            else
                                            {
                                                
                                                if (Blocks.Count > 0 && Blocks[Blocks.Count - 1].Dice == -1)
                                                    Blocks[Blocks.Count - 1].RR = true;

                                                if(nextRed)
                                                    rba.Red = true;

                                                Blocks.Add(rba);

                                                Items.Add(new ReplayItem(ReplayItemType.Block, Blocks.Count - 1, localIdToGlobalId[ba.PlayerId]));
                                                lastItemCausingArmorTest = Items.Count - 1;

                                                nextRed = false;
                                            }

                                            if(ba.PlayerId==7)
                                            {
                                                bool breakMe = true;
                                            }

                                        }
                                        else // this is the selection of dices
                                        {
                                            
                                            Blocks[Blocks.Count - 1].Dice = ReplayBlockAction.ParseDices(bar.CoachChoices.ListDices)[0];
                                        }
                                        break;
                                    case ReplayItemType.Injury:
                                        if(bar.CoachChoices.ListDices!=null)
                                        { 
                                            ReplayInjuryAction ria = new ReplayInjuryAction(lastItemCausingArmorTest, ReplayActionBase.ParseDices(bar.CoachChoices.ListDices));
                                            Injuries.Add(ria);
                                            //System.Diagnostics.Debug.Assert(ria.Roll.Count > 1);
                                            Items.Add(new ReplayItem(ReplayItemType.Injury, Injuries.Count - 1, localIdToGlobalId[ba.PlayerId]));
                                        }
                                        break;
                                    case ReplayItemType.CasualtyRoll:
                                        if (bar.CoachChoices.ListDices != null)
                                        {
                                            ReplayInjuryAction cia = new ReplayInjuryAction(lastItemCausingArmorTest, ReplayActionBase.ParseDices(bar.CoachChoices.ListDices));

                                            // For some reason have double values... remove the last
                                            cia.Roll.RemoveAt(cia.Roll.Count - 1);
                                            Casualties.Add(cia);
                                            Items.Add(new ReplayItem(ReplayItemType.CasualtyRoll, Casualties.Count - 1, localIdToGlobalId[ba.PlayerId]));
                                        }
                                        break;
                                    case ReplayItemType.Push:
                                        if (bar.IsOrderCompleted == 1)
                                        {
                                            ReplayMoveAction rma3 = new ReplayMoveAction(
                                                   new ReplayActionPosition(ba.Order.CellTo.Cell),
                                                   new ReplayActionPosition(bar.CoachChoices.ListCells[0]));
                                            Moves.Add(rma3);
                                            int pid3 = -1;
                                            localIdToGlobalId.TryGetValue(ba.PlayerId, out pid3);
                                            Items.Add(new ReplayItem(type, Moves.Count - 1, pid3));
                                            
                                            positionMap[ba.Order.CellTo.Cell.ToString()] = ba.PlayerId;
                                        }
                                        break;
                                    case ReplayItemType.FollowUp:
                                        if (bar.IsOrderCompleted == 1 && bar.ResultType == 0)
                                        {

                                            int pid3 = -1;
                                            localIdToGlobalId.TryGetValue(ba.PlayerId, out pid3);
                                            //if (positionMap[ba.Order.CellTo.Cell.ToString()] != ba.PlayerId)
                                            {
                                                ReplayMoveAction rma3 = new ReplayMoveAction(
                                                       new ReplayActionPosition(ba.Order.CellTo.Cell),
                                                       new ReplayActionPosition(bar.CoachChoices.ListCells[0]));
                                                Moves.Add(rma3);
                                                Items.Add(new ReplayItem(type, Moves.Count - 1, pid3));

                                                positionMap[ba.Order.CellTo.Cell.ToString()] = ba.PlayerId;
                                            }
                                        }
                                        break;
                                    case ReplayItemType.Move:
                                        

                                        if (ba.Order != null && ba.Order.CellTo != null)
                                            positionMap[ba.Order.CellTo.Cell.ToString()] = ba.PlayerId;

                                        int pid = -1;
                                        //if (ba.Order.CellFrom.x != ba.Order.CellTo.Cell.x ||
                                        //    ba.Order.CellFrom.y != ba.Order.CellTo.Cell.y)
                                        {
                                            

                                            localIdToGlobalId.TryGetValue(ba.PlayerId, out pid);

                                            // Is this same mover as last time?
                                            if (Moves.Count > 0 && Items.Count > 0 &&
                                                Items[Items.Count - 1].AID == (int)ReplayItemType.Move &&
                                                Items[Items.Count - 1].PID == pid)
                                            {
                                                Moves[Moves.Count - 1].AddStep(new ReplayActionPosition(ba.Order.CellTo.Cell));
                                            }
                                            else
                                            {

                                                ReplayMoveAction rma = new ReplayMoveAction(
                                                    new ReplayActionPosition(ba.Order.CellFrom),
                                                    new ReplayActionPosition(ba.Order.CellTo.Cell));
                                                Moves.Add(rma);

                                                Items.Add(new ReplayItem(ReplayItemType.Move, Moves.Count - 1, pid));
                                            }
                                        }
                                        break;
                                    default:
                                        if (bar.IsOrderCompleted == 0)
                                            continue;

                                        if (ba.Order != null && ba.Order.CellTo != null && ba.Order.CellTo.Cell != null)
                                            positionMap[ba.Order.CellTo.Cell.ToString()] = ba.PlayerId;

                                        if (bar.RollType != 0 && bar.CoachChoices.ListDices != null)
                                        {
                                            ReplayRollAction rda = new ReplayRollAction(bar.Requirement - GetModifierSum(bar.ListModifiers), ReplayActionBase.ParseDices(bar.CoachChoices.ListDices),ba.Order.CellTo.Cell, bar.IsOrderCompleted == 0);
                                            Rolls.Add(rda);
                                            if(localIdToGlobalId.ContainsKey(ba.PlayerId))
                                                Items.Add(new ReplayItem(type, Rolls.Count - 1, localIdToGlobalId[ba.PlayerId]));
                                            else
                                                Items.Add(new ReplayItem(type, Rolls.Count - 1, -1));
                                   
                                        }
                                        else
                                        {
                                            
                                            ReplayMoveAction rma2 = new ReplayMoveAction(
                                                new ReplayActionPosition(ba.Order.CellFrom),
                                                new ReplayActionPosition(ba.Order.CellTo.Cell));
                                            Moves.Add(rma2);
                                            pid = -1;
                                            localIdToGlobalId.TryGetValue(ba.PlayerId, out pid);
                                            Items.Add(new ReplayItem(type, Moves.Count - 1, pid));
                                        }
                                        break;     


                                }
                                switch(type)
                                {
                                    case ReplayItemType.Dodge:
                                    case ReplayItemType.Leap:
                                    case ReplayItemType.Block:
                                    case ReplayItemType.GFI:
                                    case ReplayItemType.Foul:
                                        
                                        lastItemCausingArmorTest = Items.Count-1;
                                        break;
                                }
                               


                            }

                        }

                        

                    }
                }


                if (step.BoardState != null && step.BoardState.Ball != null && step.BoardState.Ball.Cell != null)
                {
                    if (step.BoardState.Ball.Cell.x != ballPos.X ||
                        step.BoardState.Ball.Cell.y != ballPos.Y)
                    {
                        ballPos = new ReplayActionPosition();
                        ballPos.X = step.BoardState.Ball.Cell.x;
                        ballPos.Y = step.BoardState.Ball.Cell.y;
                        ReplayBallAction ballAction = new ReplayBallAction();
                        ballAction.Pos = new ReplayActionPosition();
                        ballAction.Pos.X = step.BoardState.Ball.Cell.x;
                        ballAction.Pos.Y = step.BoardState.Ball.Cell.y;
                        ballAction.IsBallHeld = step.BoardState.Ball.IsHeld > 0;
                        if (ballAction.IsBallHeld)
                        {
                            try
                            {
                                ballAction.PID = localIdToGlobalId[positionMap[ballAction.Pos.ToString()]];
                            }
                            catch { ballAction.IsBallHeld = false; }
                        }
                        else ballAction.PID = -1;
                        Balls.Add(ballAction);
                        Items.Add(new ReplayItem(ReplayItemType.BallAction, Balls.Count - 1, ballAction.PID));
                    }
                }
            }
		}
        int GetModifierSum(List<DiceModifier> modifiers)
        {
            int modsum = 0;
            foreach (DiceModifier mod in modifiers)
            {
                modsum += (mod.Value);
            }
            return modsum;
        }
	}
}

