twoplot <- function(w, e, param, country){
  param <- paste(param)
  ctry <- paste(country, collapse = " and ")
  param <- paste(param, "(", ctry, ")")
  
  plot(x= w$time, y=w$total, col='black', type='bar', 
       #xlim = c(min(w$time), max(w$time)),
       ylim = c(0.9*min(w$total), 1.1*max(w$total)),
       main= param, xlab='Date', ylab='total', xaxt='n');
  
  #e <- e[e$cat=="total",]  
  
  points(x=w$time, y=w$total, col='green', type='l', lwd=2)
  par(new=T)
  plot(x=e$time, y=e$total, ylim=c(min(e$total),1.1*max(e$total)),
       col='black', type='bar', lty=2,
       xaxt='n', axes=F,xlab='', ylab='');
  
  points(x=e$time, y=e$total, col='red', type='l', lwd=2, lty=2)
  axis(4, pretty(c(min(e$total), 1.1*max(e$total))), col='red')
  
  mtext(side=2, line=4, 'close ($)')
  
  locs <- tapply(X=w$time, FUN=min, INDEX=format(w$time, '%Y%m'))
  at = w$time %in% locs
  at = at & format(w$time, '%m') %in% c('01', '04', '07', '10')
  axis(side=1, at=w$time[ at ],   labels=format(w$time[at], '%b-%y'))
  
  abline(v=w$time[at], col='grey', lwd=0.5)
  #legend(x=as.Date('2012-03-01'), y=35, legend=c('total', 'Positive etion'), col=c(rep('blue',2) , lwd=c(1.5, 3.5)));
  
}